from django.contrib.auth.models import User, Group
from rest_framework.test import APITestCase, APIClient
from main.models import Skill 

LIST = "/api/v1/skills/"
def DETAIL(pk): return f"/api/v1/skills/{pk}/"
def STAR(pk): return f"/api/v1/skills/{pk}/star/"  

VALID = {"name": "Django", "category": "backend", "proficiency": "beginner", "icon_url": ""}


class SkillAPITests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser("owner", password="pw12345!")
        self.user = User.objects.create_user("biasa", password="pw12345!")
        self.editor = User.objects.create_user("editor", password="pw12345!")
        self.editor.groups.add(Group.objects.get_or_create(name="Editor")[0])  
        self.skill = Skill.objects.create(**VALID)

    def login(self, u):
        self.client.login(username=u.username, password="pw12345!")

    # --- Pengunjung ---
    def test_visitor_can_read(self):
        self.assertEqual(self.client.get(LIST).status_code, 200)
        self.assertEqual(self.client.get(DETAIL(self.skill.pk)).status_code, 200)

    def test_visitor_cannot_write(self):
        n = Skill.objects.count()
        self.assertEqual(self.client.post(LIST, VALID, format="json").status_code, 403)
        self.assertEqual(self.client.patch(DETAIL(self.skill.pk), {"proficiency": "advanced"}, format="json").status_code, 403)
        self.assertEqual(self.client.delete(DETAIL(self.skill.pk)).status_code, 403)
        self.assertEqual(Skill.objects.count(), n)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.proficiency, "beginner")

    # --- Pengguna biasa ---
    def test_regular_user_cannot_write(self):
        self.login(self.user)
        n = Skill.objects.count()
        self.assertEqual(self.client.post(LIST, VALID, format="json").status_code, 403)
        self.assertEqual(self.client.patch(DETAIL(self.skill.pk), {"proficiency": "advanced"}, format="json").status_code, 403)
        self.assertEqual(self.client.delete(DETAIL(self.skill.pk)).status_code, 403)
        self.assertEqual(Skill.objects.count(), n)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.proficiency, "beginner")

    # --- Editor ---
    def test_editor_can_patch_not_create_or_delete(self):
        self.login(self.editor)
        r = self.client.patch(DETAIL(self.skill.pk), {"proficiency": "advanced"}, format="json")
        self.assertEqual(r.status_code, 200)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.proficiency, "advanced")

        n = Skill.objects.count()
        self.assertEqual(self.client.post(LIST, VALID, format="json").status_code, 403)
        self.assertEqual(self.client.delete(DETAIL(self.skill.pk)).status_code, 403)
        self.assertEqual(Skill.objects.count(), n)

    # --- Pemilik ---
    def test_owner_can_create_and_delete(self):
        self.login(self.owner)
        r = self.client.post(LIST, {**VALID, "name": "Flask"}, format="json")
        self.assertEqual(r.status_code, 201)
        self.assertTrue(Skill.objects.filter(name="Flask").exists())
        r = self.client.delete(DETAIL(self.skill.pk))
        self.assertEqual(r.status_code, 204)
        self.assertFalse(Skill.objects.filter(pk=self.skill.pk).exists())

    def test_404(self):
        self.assertEqual(self.client.get(DETAIL("00000000-0000-0000-0000-000000000000")).status_code, 404)

    # --- Validasi ---
    def test_invalid_input_400_and_strip_tags(self):
        self.login(self.owner)
        n = Skill.objects.count()
        r = self.client.post(LIST, {**VALID, "name": "   "}, format="json")
        self.assertEqual(r.status_code, 400)
        self.assertEqual(Skill.objects.count(), n)

        r = self.client.post(LIST, {**VALID, "name": "<b>Rust</b>"}, format="json")
        self.assertEqual(r.status_code, 201)
        self.assertTrue(Skill.objects.filter(name="Rust").exists())

    # --- Pencarian ---
    def test_search_query_param(self):
        Skill.objects.create(**{**VALID, "name": "Postgres"})
        r = self.client.get(LIST, {"q": "Postg"}) 
        self.assertEqual(r.status_code, 200)
        self.assertEqual([s["name"] for s in r.data], ["Postgres"])

    # --- Star ---
    def test_star_requires_login(self):
        self.assertEqual(self.client.post(STAR(self.skill.pk)).status_code, 403)
        self.assertEqual(self.client.get(DETAIL(self.skill.pk)).data["star_count"], 0)

    def test_star_toggle(self):
        self.login(self.user)
        self.assertEqual(self.client.post(STAR(self.skill.pk)).status_code, 200)
        d = self.client.get(DETAIL(self.skill.pk)).data
        self.assertEqual(d["star_count"], 1)
        self.assertTrue(d["is_starred"])

        self.assertEqual(self.client.post(STAR(self.skill.pk)).status_code, 200)
        d = self.client.get(DETAIL(self.skill.pk)).data
        self.assertEqual(d["star_count"], 0)
        self.assertFalse(d["is_starred"])

    # --- CSRF ---
    def test_csrf_enforced(self):
        c = APIClient(enforce_csrf_checks=True)
        c.login(username="owner", password="pw12345!")
        n = Skill.objects.count()
        r = c.post(LIST, VALID, format="json")
        self.assertEqual(r.status_code, 403)
        self.assertEqual(Skill.objects.count(), n)