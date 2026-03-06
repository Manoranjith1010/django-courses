from django.apps import AppConfig


class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.courses'
    verbose_name = 'Courses'

    def ready(self):
        # Register signal handlers so the nav-menu cache is cleared
        # whenever a Topic is saved or deleted.
        import apps.courses.signals  # noqa: F401
