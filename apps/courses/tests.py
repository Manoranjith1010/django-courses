from django.test import TestCase
from .models import Course

# Create your tests here.
class CourseTest(TestCase):
    def test_course_creation(self):
        self.assertEqual(Course.objects.count(), 0)
