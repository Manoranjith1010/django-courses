# LaunchDev — Learning Management System

> A production-ready, full-featured Learning Management System built with **Django 5.1** and **Python 3.13**. Educators publish courses; students enroll, watch lectures, track progress, earn certificates, and leave reviews — all in a polished Bootstrap 5 UI.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.1.4-092E20?logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.x-4479A1?logo=mysql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?logo=bootstrap&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Database Configuration](#database-configuration)
- [URL Reference](#url-reference)
- [Data Models](#data-models)
- [Contributing](#contributing)
- [License](#license)

---

## Features

### Students
| Feature | Details |
|---|---|
| **Authentication** | Sign up, login, password reset via email |
| **Social Login** | One-click OAuth with Google & GitHub |
| **Course Enrollment** | Browse, filter by topic, and enroll in courses |
| **Lecture Player** | YouTube embed or direct file playback |
| **Progress Tracking** | Mark lectures complete via AJAX; per-course progress bar |
| **Certificates** | Auto-issued with unique UUID on course completion |
| **Course Reviews** | Rate (1–5 stars) and review completed courses |
| **User Profiles** | Avatar upload with live preview, bio, personal info |

### Instructors & Admins
| Feature | Details |
|---|---|
| **Course Management** | Create courses with slug, image, description, topics |
| **Lecture Management** | YouTube ID or file-upload lectures, previewable flag |
| **Instructor Assignment** | Each course linked to an instructor account |
| **User Management** | Manage enrollments, accounts, and permissions |
| **Topic Categories** | Hierarchical topics with slugs and SEO metadata |
| **Cache Invalidation** | Topic nav menu cache auto-cleared on save/delete via signals |
| **Social Auth Config** | Configure Google/GitHub OAuth from the admin panel |

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Django 5.1.4, Python 3.13 |
| **Frontend** | Bootstrap 5, vanilla JS (no jQuery), CSS Grid |
| **Database** | MySQL 8.x (via `mysqlclient`) |
| **Authentication** | django-allauth — email + Google + GitHub OAuth |
| **Environment** | python-dotenv (`.env` file) |
| **Caching** | Django cache framework (configurable backend) |
| **File Storage** | Local media storage (configurable for S3/cloud) |
| **Fonts** | Playfair Display, DM Sans (Google Fonts) |

---

## Project Structure

```
django-courses/
├── apps/
│   ├── core/               # User profiles, signals
│   ├── courses/            # Course, Lecture, Enrollment, Review, Certificate
│   │   ├── migrations/
│   │   ├── models.py       # Course (+ instructor FK), Lecture, Topic, Enrollment,
│   │   │                   #   LectureProgress, Review, Certificate (UUID)
│   │   ├── views.py        # Course listing, detail, lecture player, AJAX mark_complete
│   │   ├── urls.py
│   │   ├── signals.py      # Topic post_save/post_delete → cache invalidation
│   │   └── apps.py
│   └── users/              # Extended user management
├── courseproject/
│   ├── settings.py         # Credentials via os.getenv(), env-driven config
│   ├── urls.py
│   └── wsgi.py
├── templates/
│   ├── base.html           # Bootstrap 5, showToast(), custom nav
│   ├── partials/
│   │   ├── _course_card.html
│   │   ├── _lecture_sidebar.html
│   │   ├── _messages.html
│   │   └── _empty_state.html
│   ├── courses/
│   │   ├── courses.html    # CSS Grid listing with filter chips
│   │   ├── index.html      # Hero + paginated course grid
│   │   ├── lecture.html    # Lecture player + AJAX progress
│   │   └── lecture_selected.html
│   └── account/            # django-allauth overrides
├── assets/                 # Custom CSS components
├── media/                  # Uploaded course images & videos
├── .env                    # Local secrets (not committed)
├── .env.example
└── requirements.txt
```

---

## Installation

### Prerequisites

- Python 3.10+
- MySQL 8.x running locally
- Git

### Quick Start

**1. Clone the repository**
```bash
git clone https://github.com/your-org/django-courses.git
cd django-courses
```

**2. Create and activate a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**
```bash
cp .env.example .env
# Open .env and fill in your values (see Environment Variables below)
```

**5. Create the MySQL database**
```sql
CREATE DATABASE launchdev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**6. Run migrations**
```bash
python manage.py migrate
```

**7. Create a superuser**
```bash
python manage.py createsuperuser
```

**8. Start the development server**
```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser. Admin panel: http://127.0.0.1:8000/admin/

---

## Environment Variables

Create `.env` in the project root (same directory as `manage.py`). All values are loaded via `python-dotenv`.

```env
# Django
SECRET_KEY=your-very-long-random-secret-key
DEBUG=True
ALLOWED_HOSTS=*

# MySQL Database
DB_NAME=launchdev
DB_USER=root
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306

# Email (for password reset / verification)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Google OAuth (optional — configure in Django admin under Social Applications)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# GitHub OAuth (optional)
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

> **Security note:** Never commit `.env` to version control. It is listed in `.gitignore`.

---

## Database Configuration

The project uses **MySQL** by default. Settings are read from `.env`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'launchdev'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
    }
}
```

To switch to **PostgreSQL**, set `ENGINE` to `django.db.backends.postgresql` and install `psycopg2-binary`.  
For **SQLite** (development only): `django.db.backends.sqlite3` with `NAME = BASE_DIR / 'db.sqlite3'`.

---

## URL Reference

| Method | URL | Name | Description |
|---|---|---|---|
| GET | `/` | `home` | Homepage with featured courses |
| GET | `/courses/` | `courses` | Paginated listing with topic filter chips |
| GET | `/course/<slug>/` | `course-detail` | Course detail, reviews, enroll button |
| POST | `/course/<slug>/enroll/` | `enroll` | Enroll the current user |
| GET | `/course/<slug>/lecture/` | `lecture` | Lecture player (first lecture) |
| GET | `/course/<slug>/lecture/<id>/` | `lecture-selected` | Specific lecture player |
| POST | `/lecture/<id>/mark-complete/` | `mark-complete` | AJAX — mark lecture complete |
| GET | `/my-courses/` | `my-courses` | Enrolled courses dashboard |
| GET | `/search/?q=` | `search` | Full-text course search |
| GET | `/topic/<slug>/` | `topic-courses` | Filter courses by topic |
| GET | `/profile/` | `profile` | User profile page |
| GET/POST | `/profile/edit/` | `profile-edit` | Edit profile & avatar |
| GET | `/admin/` | — | Django admin dashboard |

---

## Data Models

### Course
- `course_title`, `course_slug`, `course_description`, `course_image`
- `topics` — ManyToMany → `Topic`
- `instructor` — ForeignKey → `User` (`SET_NULL`)
- `course_created_at`, active/featured flags

### Lecture
- `lecture_title`, `lecture_slug`, `lecture_description`
- `youtube_id` or file upload; `is_previewable`
- ForeignKey → `Course`

### Topic
- `topic_name`, `topic_slug`, SEO meta fields
- Post-save/delete signals clear the nav menu cache automatically

### Enrollment
- ForeignKey → `User`, ForeignKey → `Course`
- `enrolled_at`; unique constraint per user–course pair

### LectureProgress
- ForeignKey → `User`, ForeignKey → `Lecture`
- `is_completed`, `completed_at`

### Review
- ForeignKey → `User`, ForeignKey → `Course`
- `rating` (1–5), `comment`, `created_at`

### Certificate
- ForeignKey → `User`, ForeignKey → `Course`
- `certificate_id` — `UUIDField(default=uuid.uuid4, unique=True)`
- `issued_at`

---

## Contributing

1. Fork the repository
2. Create a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes
   ```bash
   git commit -m "feat: describe your change"
   ```
4. Push and open a Pull Request
   ```bash
   git push origin feature/your-feature-name
   ```

Ensure all tests pass before submitting:
```bash
python manage.py test
```

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

*Built with Django 5.1 · Bootstrap 5 · MySQL · django-allauth*

