from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command

from .models import Degree, User
from .management.commands.seed_admin import DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_USERNAME


class AccountFlowTests(TestCase):
    def setUp(self):
        self.degree = Degree.objects.create(degree_title="Computer Science")
        self.admin_user = User.objects.create_user(
            username="admin01",
            password="admin-pass-123",
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
            role=User.Role.ADMIN,
            is_staff=True,
        )
        self.student_user = User.objects.create_user(
            username="student01",
            password="student-pass-123",
            email="student@example.com",
            first_name="Student",
            last_name="User",
            role=User.Role.STUDENT,
            student_no="STU-001",
            degree=self.degree,
        )

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_admin_can_access_student_list(self):
        self.client.login(username="admin01", password="admin-pass-123")
        response = self.client.get(reverse("student_list"))
        self.assertEqual(response.status_code, 200)

    def test_student_is_redirected_from_admin_page(self):
        self.client.login(username="student01", password="student-pass-123")
        response = self.client.get(reverse("student_list"))
        self.assertRedirects(response, reverse("student_dashboard"))

    def test_admin_create_student_page_loads(self):
        self.client.login(username="admin01", password="admin-pass-123")
        response = self.client.get(reverse("student_create"))
        self.assertEqual(response.status_code, 200)

    def test_admin_can_view_student_detail(self):
        self.client.login(username="admin01", password="admin-pass-123")
        response = self.client.get(reverse("student_detail", args=[self.student_user.pk]))
        self.assertEqual(response.status_code, 200)

    def test_degree_seeder_creates_records(self):
        Degree.objects.all().delete()
        call_command("seed_degrees")
        self.assertGreater(Degree.objects.count(), 0)

    def test_student_seeder_creates_requested_records(self):
        User.objects.filter(role=User.Role.STUDENT).delete()
        call_command("seed_students", count=5, password="SeedPass123!")
        self.assertEqual(User.objects.filter(role=User.Role.STUDENT).count(), 5)

    def test_admin_seeder_creates_default_admin_account(self):
        User.objects.filter(username=DEFAULT_ADMIN_USERNAME).delete()
        call_command("seed_admin")
        admin_user = User.objects.get(username=DEFAULT_ADMIN_USERNAME)
        self.assertEqual(admin_user.email, DEFAULT_ADMIN_EMAIL)
        self.assertEqual(admin_user.role, User.Role.ADMIN)
        self.assertTrue(admin_user.is_staff)

    def test_student_seeder_also_ensures_default_admin_account(self):
        User.objects.filter(username=DEFAULT_ADMIN_USERNAME).delete()
        call_command("seed_students", count=1, password="SeedPass123!")
        self.assertTrue(User.objects.filter(username=DEFAULT_ADMIN_USERNAME, role=User.Role.ADMIN).exists())
