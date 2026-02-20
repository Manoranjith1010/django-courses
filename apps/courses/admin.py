from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from apps.core.admin import admin_site
from .models import Topic, Course, Lecture, Enroll, LectureProgress, Review


class TopicAdmin(admin.ModelAdmin):
    list_display = ('topic_title', 'topic_slug', 'topic_is_active')
    list_editable = ('topic_slug', 'topic_is_active')
    list_filter = ('topic_is_active', 'topic_created_at')
    list_per_page = 10
    search_fields = ('topic_title', 'topic_description')
    prepopulated_fields = {"topic_slug": ("topic_title", )}


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_title', 'course_slug', 'course_is_active', 'course_is_featured')
    list_editable = ('course_slug', 'course_is_active', 'course_is_featured')
    list_filter = ('course_is_active', 'course_is_featured', 'course_created_at')
    list_per_page = 10
    search_fields = ('course_title', 'course_description')
    prepopulated_fields = {"course_slug": ("course_title", )}
    filter_horizontal = ('course_topic',)  # Better UI for ManyToMany


class LectureAdminForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        course = cleaned_data.get("course")
        lecture_slug = cleaned_data.get("lecture_slug")

        if course and lecture_slug:
            exists = (
                Lecture.objects.filter(course=course, lecture_slug=lecture_slug)
                .exclude(pk=self.instance.pk)
                .exists()
            )
            if exists:
                raise ValidationError(
                    {
                        "lecture_slug": "This slug already exists for the selected course."
                    }
                )

        return cleaned_data


class LectureAdmin(admin.ModelAdmin):
    form = LectureAdminForm
    list_display = ('lecture_title', 'course', 'lecture_slug', 'lecture_previewable')
    list_editable = ('lecture_slug', 'lecture_previewable')
    list_filter = ('lecture_previewable', 'lecture_created_at', 'course')
    list_per_page = 10
    search_fields = ('lecture_title', 'lecture_description', 'course__course_title')
    prepopulated_fields = {"lecture_slug": ("lecture_title", )}
    exclude = ('lecture_video',)
    # Performance optimizations
    list_select_related = ('course',)


class EnrollAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_date')
    list_filter = ('enrolled_date', 'course')
    list_per_page = 10
    search_fields = ('user__username', 'user__email', 'course__course_title')
    # Performance optimizations
    list_select_related = ('user', 'course')
    date_hierarchy = 'enrolled_date'


class LectureProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lecture', 'completed', 'completed_at', 'last_accessed')
    list_filter = ('completed', 'completed_at')
    list_per_page = 20
    search_fields = ('user__username', 'lecture__lecture_title')
    readonly_fields = ('last_accessed',)
    # Performance optimizations
    list_select_related = ('user', 'lecture', 'lecture__course')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    list_per_page = 20
    search_fields = ('user__username', 'course__course_title', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    # Performance optimizations
    list_select_related = ('user', 'course')


# Register models with both the default admin site and the custom LMS admin
for site in (admin.site, admin_site):
    site.register(Topic, TopicAdmin)
    site.register(Course, CourseAdmin)
    site.register(Lecture, LectureAdmin)
    site.register(Enroll, EnrollAdmin)
    site.register(LectureProgress, LectureProgressAdmin)
    site.register(Review, ReviewAdmin)

