from django.forms import ModelForm, TextInput, Textarea, URLInput, Select

from main.models import Project, Skill


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "category", "proficiency", "icon_url"]

        labels = {
            "name": "Nama Skill",
            "category": "Kategori",
            "proficiency": "Tingkat Kemahiran",
            "icon_url": "URL Ikon",
        }

        widgets = {
            "name": TextInput(
                attrs={
                    "placeholder": "Django",
                    "maxlength": 100,
                }
            ),
            "category": Select(),
            "proficiency": Select(),
            "icon_url": URLInput(
                attrs={
                    "placeholder": "https://cdn.example.com/icons/django.svg",
                }
            ),
        }