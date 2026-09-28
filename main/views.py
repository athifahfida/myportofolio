import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from main.forms import ProjectForm, SkillForm
from main.models import Experience, Certification, Project, Skill


def is_editor(user):
    return user.groups.filter(name='Editor').exists()


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Athifah Mufidah",
        "npm": "2506612045",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Athifah Mufidah",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_certification(request):
    context = {
        "certification_list": Certification.objects.all(),
    }
    return render(request, "certification.html", context)


@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Athifah Mufidah",
        "form": form,
    }
    return render(request, "projects_form.html", context)


@login_required(login_url="/login/")
def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied

    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil diperbarui!")
        return redirect("main:show_projects")

    context = {
        "name": "Athifah Mufidah",
        "form": form,
    }
    return render(request, "projects_form.html", context)


def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Athifah Mufidah",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize(
        "json", projects, use_natural_foreign_keys=True
    )
    return HttpResponse(projects_json, content_type="application/json")


@login_required(login_url="/login/")
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if not request.user.is_superuser:
        raise PermissionDenied
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")


def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Athifah Mufidah",
        "form": form,
    }
    return render(request, "register.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Athifah Mufidah",
        "form": form,
    }
    return render(request, "login.html", context)


# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi star
@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")


# ---------------------------- SKILL (AJAX) ----------------------------

def show_skill(request):
    context = {
        "name": "Athifah Mufidah",
        "form": SkillForm() if request.user.is_superuser else None,
    }
    return render(request, "skill.html", context)


def _skill_to_dict(skill, user):
    stars = list(skill.starred_by.all())
    return {
        "id": str(skill.id),
        "name": skill.name,
        "category": skill.category,
        "category_display": skill.get_category_display(),
        "proficiency": skill.proficiency,
        "proficiency_display": skill.get_proficiency_display(),
        "icon_url": skill.icon_url,
        "star_count": len(stars),
        "is_starred": user.is_authenticated
        and any(u.pk == user.pk for u in stars),
    }


def get_skills_json(request):
    q = request.GET.get("q", "").strip()
    skills = Skill.objects.prefetch_related("starred_by").order_by("-timestamp")
    if q:
        skills = skills.filter(name__icontains=q)

    user = request.user
    return JsonResponse(
        {
            "skills": [_skill_to_dict(s, user) for s in skills],
            "is_authenticated": user.is_authenticated,
            "can_add": user.is_superuser,
            "can_edit": user.is_authenticated
            and (user.is_superuser or is_editor(user)),
        }
    )


@require_POST
def create_skill_ajax(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return JsonResponse(
            {"message": "Kamu tidak punya izin untuk menambah skill."},
            status=403,
        )

    form = SkillForm(request.POST)
    if form.is_valid():
        skill = form.save()
        return JsonResponse(
            {
                "message": "Skill berhasil ditambahkan!",
                "skill": _skill_to_dict(skill, request.user),
            },
            status=201,
        )

    errors = {field: list(errs) for field, errs in form.errors.items()}
    return JsonResponse(
        {"message": "Data tidak valid.", "errors": errors}, status=400
    )


@require_POST
def toggle_star_skill(request, skill_id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"message": "Login dulu untuk memberi star."}, status=403
        )

    skill = get_object_or_404(Skill, pk=skill_id)
    if skill.starred_by.filter(pk=request.user.pk).exists():
        skill.starred_by.remove(request.user)
        starred = False
    else:
        skill.starred_by.add(request.user)
        starred = True

    return JsonResponse(
        {"starred": starred, "star_count": skill.starred_by.count()}
    )


@login_required(login_url="/login/")
def create_skill(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = SkillForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill baru berhasil ditambahkan!")
        return redirect("main:show_skill")

    context = {
        "name": "Athifah Mufidah",
        "form": form,
    }
    return render(request, "skill_form.html", context)


@login_required(login_url="/login/")
def update_skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)

    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied

    form = SkillForm(request.POST or None, instance=skill)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill berhasil diperbarui!")
        return redirect("main:show_skill")

    context = {
        "name": "Athifah Mufidah",
        "form": form,
    }
    return render(request, "skill_form.html", context)


@login_required(login_url="/login/")
def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)

    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill berhasil dihapus!")
        return redirect("main:show_skill")

    return redirect("main:show_skill")