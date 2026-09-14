from django.shortcuts import render

from main.models import Experience, Certification


def show_main(request):
    context = {
        "name": "Athifah Mufidah",
        "npm": "2506612045",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
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