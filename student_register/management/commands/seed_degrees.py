from django.core.management.base import BaseCommand

from student_register.models import Degree


DEFAULT_DEGREES = [
    "Bachelor of Science in Computer Science",
    "Bachelor of Science in Information Technology",
    "Bachelor of Science in Information Systems",
    "Bachelor of Science in Accountancy",
    "Bachelor of Science in Business Administration",
    "Bachelor of Science in Hospitality Management",
    "Bachelor of Elementary Education",
    "Bachelor of Secondary Education",
]


class Command(BaseCommand):
    help = "Seed default degree records for the student management system."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete all existing degrees before seeding defaults.",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            deleted_count, _ = Degree.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted_count} existing degree-related record(s)."))

        created = 0
        existing = 0

        for degree_title in DEFAULT_DEGREES:
            _, was_created = Degree.objects.get_or_create(degree_title=degree_title)
            if was_created:
                created += 1
            else:
                existing += 1

        self.stdout.write(self.style.SUCCESS(f"Degree seeding complete. Created: {created}, Existing: {existing}"))
