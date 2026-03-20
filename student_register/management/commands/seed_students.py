from datetime import date, timedelta

from django.core.management.base import BaseCommand

from student_register.management.commands.seed_degrees import DEFAULT_DEGREES
from student_register.models import Degree, User


FIRST_NAMES = [
    "Liam", "Noah", "Oliver", "Elijah", "James", "William", "Benjamin", "Lucas", "Henry", "Alexander",
    "Olivia", "Emma", "Charlotte", "Amelia", "Sophia", "Isabella", "Ava", "Mia", "Evelyn", "Luna",
    "Daniel", "Matthew", "Joseph", "Samuel", "David", "John", "Michael", "Ethan", "Sebastian", "Jack",
    "Harper", "Ella", "Aria", "Scarlett", "Grace", "Chloe", "Camila", "Penelope", "Riley", "Layla",
]

MIDDLE_NAMES = [
    "Reed", "Cole", "Blake", "Dean", "Jude", "Lane", "Quinn", "Sage", "Skye", "Drew",
    "Faith", "Rose", "Jane", "Hope", "Claire", "Mae", "Kate", "Joy", "Faye", "Anne",
]

LAST_NAMES = [
    "Anderson", "Bennett", "Carter", "Diaz", "Edwards", "Flores", "Garcia", "Hughes", "Ibrahim", "Jenkins",
    "Kim", "Lopez", "Mitchell", "Nguyen", "Owens", "Patel", "Quintero", "Robinson", "Santos", "Turner",
    "Usman", "Valdez", "Walker", "Xu", "Young", "Zimmerman", "Reyes", "Cruz", "Morgan", "Parker",
]

CITY_NAMES = ["Manila", "Quezon City", "Cebu City", "Davao City", "Iloilo City", "Baguio", "Pasig", "Makati"]
PROVINCES = ["Metro Manila", "Cebu", "Davao del Sur", "Iloilo", "Benguet", "Laguna", "Bulacan", "Batangas"]
SECTIONS = ["A", "B", "C", "D"]
GUARDIAN_RELATIONSHIPS = ["Mother", "Father", "Guardian", "Aunt", "Uncle", "Sibling"]
ENROLLMENT_STATUSES = [
    User.EnrollmentStatus.ENROLLED,
    User.EnrollmentStatus.REGULAR,
    User.EnrollmentStatus.ON_LEAVE,
]


class Command(BaseCommand):
    help = "Seed demo student accounts with unique names, usernames, and student numbers."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=100,
            help="Number of student accounts to create. Default is 100.",
        )
        parser.add_argument(
            "--password",
            default="password",
            help="Default password for all seeded student accounts.",
        )
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing student accounts before seeding new ones.",
        )

    def handle(self, *args, **options):
        count = max(options["count"], 0)
        password = options["password"]

        for degree_title in DEFAULT_DEGREES:
            Degree.objects.get_or_create(degree_title=degree_title)

        if options["reset"]:
            deleted_count, _ = User.objects.filter(role=User.Role.STUDENT).delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted_count} existing student-related record(s)."))

        degrees = list(Degree.objects.order_by("degree_title"))
        if not degrees:
            self.stdout.write(self.style.ERROR("No degrees available for assignment."))
            return

        start_index = User.objects.filter(role=User.Role.STUDENT).count() + 1
        created = 0

        for number in range(start_index, start_index + count):
            first_name = FIRST_NAMES[(number - 1) % len(FIRST_NAMES)]
            middle_name = MIDDLE_NAMES[((number - 1) // len(FIRST_NAMES)) % len(MIDDLE_NAMES)]
            last_name = LAST_NAMES[((number - 1) // (len(FIRST_NAMES) * len(MIDDLE_NAMES))) % len(LAST_NAMES)]
            username = f"student{number:03d}"
            email = f"{username}@studenthub.local"
            student_no = f"2026-{number:04d}"
            degree = degrees[(number - 1) % len(degrees)]
            birth_date = date(2000, 1, 1) + timedelta(days=(number - 1) * 45)
            admission_date = date(2024, 8, 1) + timedelta(days=(number - 1) % 25)
            year_level = list(User.YearLevel.values)[(number - 1) % 4]
            city = CITY_NAMES[(number - 1) % len(CITY_NAMES)]
            province = PROVINCES[(number - 1) % len(PROVINCES)]
            guardian_relationship = GUARDIAN_RELATIONSHIPS[(number - 1) % len(GUARDIAN_RELATIONSHIPS)]
            status = ENROLLMENT_STATUSES[(number - 1) % len(ENROLLMENT_STATUSES)]

            if User.objects.filter(username=username).exists():
                continue

            User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                student_no=student_no,
                date_of_birth=birth_date,
                birth_place=city,
                gender=User.Gender.MALE if number % 2 else User.Gender.FEMALE,
                nationality="Filipino",
                phone_number=f"0917{number:07d}"[-11:],
                address_line=f"{100 + number} Mabini Street",
                city=city,
                state_province=province,
                postal_code=f"{1000 + (number % 900):04d}",
                country="Philippines",
                degree=degree,
                admission_date=admission_date,
                academic_year="2026-2027",
                year_level=year_level,
                section=SECTIONS[(number - 1) % len(SECTIONS)],
                enrollment_status=status,
                guardian_name=f"{first_name} {last_name} Sr.",
                guardian_relationship=guardian_relationship,
                guardian_phone=f"0919{number:07d}"[-11:],
                emergency_contact_name=f"{middle_name} {last_name}",
                emergency_contact_relationship="Relative",
                emergency_contact_phone=f"0998{number:07d}"[-11:],
                notes="Seeded demo student record for development and testing.",
                role=User.Role.STUDENT,
                is_active=True,
            )
            created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Student seeding complete. Created: {created}, Requested: {count}, Default password: {password}"
            )
        )
