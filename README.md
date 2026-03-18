# Student Project

A Django student management application with role-based accounts for admins and students.

## What's New

- Refactored to use clean project and app names:
  - `student_project/`
  - `student_register/`
- Switched the project database to SQLite
- Added a custom `User` model for account-based access
- Added role support for:
  - `admin`
  - `student`
- Added account-related routes for:
  - login
  - logout
  - admin dashboard
  - student dashboard
  - student account management
  - degree management
  - profile page

## Tech Stack

- Python
- Django
- SQLite
- django-crispy-forms
- crispy-bootstrap5
- Bootstrap 5

## Current Data Model

- `User`
  - extends Django `AbstractUser`
  - supports `admin` and `student` roles
  - stores `student_no`, `middle_name`, and `degree`
- `Degree`
  - stores available degree/program names

## Main Routes

- `/` - app entry point
- `/login/` - login page
- `/logout/` - logout
- `/admin/dashboard/` - admin dashboard
- `/student/dashboard/` - student dashboard
- `/students/` - student account list
- `/students/new/` - create student account
- `/degrees/` - degree management
- `/profile/` - logged-in user profile
- `/admin/` - Django admin

## Important Note About Database Changes

This project now uses a custom Django user model:

- `AUTH_USER_MODEL = "student_register.User"`

Because of that, if you are coming from the older version of this project, you should use a fresh SQLite database before running migrations.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create migrations:

```bash
python manage.py makemigrations
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Create an admin account:

```bash
python manage.py createsuperuser
```

6. Start the development server:

```bash
python manage.py runserver
```

## Useful Commands

Install dependencies:

```bash
pip install -r requirements.txt
```

Create new migrations after model changes:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

Create admin user:

```bash
python manage.py createsuperuser
```

Run development server:

```bash
python manage.py runserver
```

Run tests:

```bash
python manage.py test
```

Seed default degrees:

```bash
python manage.py seed_degrees
```

Reset and reseed degrees:

```bash
python manage.py seed_degrees --reset
```

Seed 100 student accounts:

```bash
python manage.py seed_students
```

Seed a custom number of student accounts:

```bash
python manage.py seed_students --count 25
```

Reset existing student accounts and seed 100 again:

```bash
python manage.py seed_students --reset
```

Seed students with a custom default password:

```bash
python manage.py seed_students --password DemoPass123!
```

## Fresh SQLite Database

If you want a clean database after the account-model refactor:

1. Stop the server.
2. Delete `db.sqlite3`.
3. Run:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Project Structure

- `student_project/` - Django project settings, URLs, WSGI, ASGI
- `student_register/` - main app for users, degrees, forms, views, and routes
- `student_register/views_auth.py` - login, logout, home, dashboard routing
- `student_register/views_admin.py` - admin dashboard, student management, degree management
- `student_register/views_student.py` - student dashboard and profile
- `student_register/forms_auth.py` - authentication form logic
- `student_register/forms_admin.py` - admin-side student and degree forms
- `student_register/forms_profile.py` - student profile form
- `student_register/decorators.py` - shared access-control decorator
- `static/` - static assets
- `requirements.txt` - Python dependencies

## Default Local URLs

- App: `http://127.0.0.1:8000/`
- Django admin: `http://127.0.0.1:8000/admin/`

## Requirements

The project dependencies are listed in `requirements.txt`.
