# Django Courses - Learning Management System

A full-featured Learning Management System (LMS) built with Django 5.x that allows educators to create and manage online courses, while students can enroll, track their progress, and leave reviews.

## Features

### For Students
- **User Authentication** - Sign up, login, password reset with email verification
- **Social Login** - One-click login with Google and GitHub (OAuth)
- **Course Enrollment** - Browse and enroll in courses
- **Progress Tracking** - Track completion status for each lecture
- **Course Reviews** - Rate and review completed courses
- **Search & Filter** - Find courses by topic or keyword
- **User Profiles** - Manage profile with bio, avatar, and personal info

### For Administrators
- **Course Management** - Create courses with multiple lectures and topics
- **Lecture Management** - Add video lectures (YouTube/file upload support)
- **User Management** - Manage student accounts and enrollments
- **Topic Categories** - Organize courses by topics with SEO metadata
- **Social Auth Config** - Configure Google/GitHub OAuth providers
- **Analytics** - View enrollment counts, ratings, and progress stats

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Django 5.1, Python 3.x |
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap 5 |
| **Database** | SQLite (default) / PostgreSQL / MySQL |
| **Authentication** | django-allauth (Google, GitHub OAuth) |
| **File Storage** | Local media / Configurable cloud storage |

## Project Structure

```
django-courses/
├── apps/
│   ├── core/           # User profiles, signals
│   ├── courses/        # Course, Lecture, Enrollment, Reviews
│   └── users/          # Extended user management
├── courseproject/      # Django settings, URLs, WSGI
├── templates/          # HTML templates
├── assets/             # Custom CSS components
└── media/              # Uploaded course images & videos
```

## Installation

### Prerequisites
- Python 3.10+
- pip (Python package manager)
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/Manoranjith1010/django-courses.git
   cd django-courses
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file in project root
   cp .env.example .env
   # Edit .env with your settings (SECRET_KEY, OAuth credentials, etc.)
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Website: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## Configuration

### Environment Variables (.env)

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=*

# Google OAuth (optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-secret

# GitHub OAuth (optional)
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-secret
```

### Database Configuration

By default, the project uses SQLite. To use PostgreSQL or MySQL, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_courses',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## API Endpoints

| URL | Description |
|-----|-------------|
| `/` | Homepage with featured courses |
| `/courses/` | All courses listing |
| `/course/<slug>/` | Course detail page |
| `/course/<slug>/enroll/` | Enroll in course |
| `/lecture/<course>/<lecture>/` | View lecture |
| `/my-courses/` | User's enrolled courses |
| `/search/?q=keyword` | Search courses |
| `/topic/<slug>/` | Courses by topic |
| `/profile/` | User profile |
| `/admin/` | Admin dashboard |

## Models

### Course
- Title, slug, description, image
- Associated topics (many-to-many)
- SEO metadata fields
- Active/featured flags

### Lecture
- Title, slug, description
- Video (YouTube ID or file upload)
- Linked to course (foreign key)
- Previewable flag

### Enrollment
- User-course relationship
- Enrollment date tracking
- Unique constraint per user-course

### LectureProgress
- User-lecture progress tracking
- Completion status and timestamp

### Review
- User-course ratings (1-5 stars)
- Comment text
- Created/updated timestamps

## Screenshots

| Homepage | Course Detail | Lecture View |
|----------|---------------|--------------|
| ![Home](docs/screenshots/home.png) | ![Course](docs/screenshots/course.png) | ![Lecture](docs/screenshots/lecture.png) |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

**Manoranjith** - [GitHub](https://github.com/Manoranjith1010)

---

If you find this project helpful, please give it a star!
