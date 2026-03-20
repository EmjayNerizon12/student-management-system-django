from django.core.management.base import BaseCommand

from student_register.models import User


DEFAULT_ADMIN_USERNAME = "admin.example"
DEFAULT_ADMIN_PASSWORD = "password"
DEFAULT_ADMIN_EMAIL = "admin@example.com"
DEFAULT_ADMIN_FIRST_NAME = "Admin"
DEFAULT_ADMIN_LAST_NAME = "Access"


def ensure_admin_account():
    user = (
        User.objects.filter(username=DEFAULT_ADMIN_USERNAME).first()
        or User.objects.filter(email=DEFAULT_ADMIN_EMAIL).first()
    )
    created = user is None

    if user is None:
        user = User.objects.create_user(
            username=DEFAULT_ADMIN_USERNAME,
            password=DEFAULT_ADMIN_PASSWORD,
            email=DEFAULT_ADMIN_EMAIL,
            first_name=DEFAULT_ADMIN_FIRST_NAME,
            last_name=DEFAULT_ADMIN_LAST_NAME,
            role=User.Role.ADMIN,
            is_staff=True,
            is_superuser=False,
            is_active=True,
        )
        return user, created

    user.username = DEFAULT_ADMIN_USERNAME
    user.email = DEFAULT_ADMIN_EMAIL
    user.first_name = DEFAULT_ADMIN_FIRST_NAME
    user.last_name = DEFAULT_ADMIN_LAST_NAME
    user.role = User.Role.ADMIN
    user.is_staff = True
    user.is_superuser = False
    user.is_active = True
    user.set_password(DEFAULT_ADMIN_PASSWORD)
    user.save()
    return user, created


class Command(BaseCommand):
    help = "Seed the default admin account for development."

    def handle(self, *args, **options):
        user, created = ensure_admin_account()
        action = "Created" if created else "Updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"{action} admin account: username={user.username}, email={user.email}, password={DEFAULT_ADMIN_PASSWORD}"
            )
        )
