from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Topic(models.Model):
    topic_title = models.CharField(max_length=50, verbose_name="Topic Title")
    topic_slug = models.SlugField(max_length=55, unique=True, db_index=True, verbose_name="Topic Slug")
    topic_description = models.TextField(blank=True, null=True, verbose_name="Topic Description")
    # topic_parent = models.ForeignKey(Topic, verbose_name="Parent Topic", on_delete=models.DO_NOTHING)
    topic_image = models.ImageField(upload_to="topics/", blank=True, null=True)
    topic_is_active = models.BooleanField(default=True, verbose_name="Is Active?")
    topic_created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    topic_updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    # Meta for SEO
    meta_topic_title = models.CharField(max_length=60, blank=True, null=True, verbose_name="SEO Topic Title (60 Characters Long)")
    meta_topic_keywords = models.TextField(blank=True, null=True, verbose_name="SEO Topic Keywords, Separated by Commas")
    meta_topic_description = models.TextField(blank=True, null=True, verbose_name="SEO Topic Description (160 characters long)")

    class Meta:
        indexes = [
            models.Index(fields=['topic_slug']),
            models.Index(fields=['topic_is_active']),
        ]

    def __str__(self):
        return self.topic_title
    

class Course(models.Model):
    course_title = models.CharField(max_length=200, verbose_name="Course Title")
    course_slug = models.SlugField(unique=True, db_index=True, verbose_name="Course Slug")
    course_description = models.TextField(blank=True, null=True, verbose_name="Course Description")
    course_topic = models.ManyToManyField(Topic, related_name="courses", verbose_name="Course Topic")
    course_image = models.ImageField(upload_to="courses/", blank=True, null=True)
    course_is_active = models.BooleanField(default=True, verbose_name="Is Active?")
    course_is_featured = models.BooleanField(default=False, verbose_name="Is Featured?")
    course_created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    course_updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    # Meta for SEO
    seo_course_title = models.CharField(max_length=60, blank=True, null=True, verbose_name="SEO Course Title (60 Characters Long)")
    seo_course_keywords = models.TextField(blank=True, null=True, verbose_name="SEO for Course Keywords, Separated by Commas")
    seo_course_description = models.TextField(blank=True, null=True, verbose_name="SEO Course Description (160 Characters Long)")
    
    class Meta:
        ordering = ('-course_created_at', )
        indexes = [
            models.Index(fields=['course_slug']),
            models.Index(fields=['course_created_at']),
            models.Index(fields=['course_is_active', 'course_is_featured']),
        ]
        
    def __str__(self):
        return self.course_title


class Lecture(models.Model):
    lecture_title = models.CharField(max_length=255, verbose_name="Lecture Title")
    lecture_slug = models.SlugField(db_index=True, verbose_name="Lecture Slug")
    lecture_description = models.TextField(blank=True, null=True, verbose_name="Lecture Description")
    course = models.ForeignKey(Course, related_name="lectures", verbose_name="Course", on_delete=models.CASCADE)
    lecture_file = models.FileField(upload_to="files/", blank=True, null=True)
    lecture_video = models.CharField(max_length=150, blank=True, null=True, verbose_name="Video ID")
    lecture_previewable = models.BooleanField(default=True, verbose_name="Is Previewable?")
    lecture_created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    lecture_updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    # Meta SEO
    seo_lecture_title = models.CharField(max_length=60, blank=True, null=True, verbose_name="SEO Lecture Title (60 Characters Long)")
    seo_lecture_keyword = models.TextField(blank=True, null=True, verbose_name="SEO Lecture Keywords, Separated by Comma")
    seo_lecture_description = models.TextField(blank=True, null=True, verbose_name="SEO Lecture Description (160 Characters Long)")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["course", "lecture_slug"],
                name="uniq_lecture_slug_per_course",
            )
        ]
        indexes = [
            models.Index(fields=['lecture_slug']),
            models.Index(fields=['course', 'lecture_slug']),
        ]

    def __str__(self):
        return self.lecture_title


class Enroll(models.Model):
    user = models.ForeignKey(User, related_name="enrollments", verbose_name="User", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name="enrollments", verbose_name="Course", on_delete=models.CASCADE)
    enrolled_date = models.DateTimeField(auto_now_add=True, verbose_name="Enrolled Date")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'course'], name='unique_user_course_enrollment')
        ]
        indexes = [
            models.Index(fields=['user', 'course']),
            models.Index(fields=['enrolled_date']),
        ]

    def __str__(self):
        return self.course.course_title


class LectureProgress(models.Model):
    """Track user progress through lectures."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lecture_progress')
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='progress')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'lecture'], name='unique_user_lecture_progress')
        ]
        verbose_name = 'Lecture Progress'
        verbose_name_plural = 'Lecture Progress'
        indexes = [
            models.Index(fields=['user', 'completed']),
            models.Index(fields=['lecture', 'completed']),
        ]

    def __str__(self):
        status = "✓" if self.completed else "○"
        return f"{status} {self.user.username} - {self.lecture.lecture_title}"


RATING_CHOICES = (
    (1, '1 - Poor'),
    (2, '2 - Fair'),
    (3, '3 - Good'),
    (4, '4 - Very Good'),
    (5, '5 - Excellent'),
)


class Review(models.Model):
    """Course reviews and ratings from users."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    comment = models.TextField(blank=True, verbose_name="Review Comment")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'course'], name='unique_user_course_review')
        ]
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['course', 'rating']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.course.course_title} ({self.rating}★)"



