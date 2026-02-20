from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone

from apps.courses.models import Course, Enroll, Review
from .models import Profile


class LMSAdminSite(admin.AdminSite):
	site_header = "LMS Admin"
	site_title = "LMS Admin"
	index_title = "Dashboard"

	def index(self, request, extra_context=None):
		extra_context = extra_context or {}

		User = get_user_model()

		extra_context["total_users"] = User.objects.count()
		extra_context["total_courses"] = Course.objects.count()
		extra_context["total_enrollments"] = Enroll.objects.count()
		extra_context["total_reviews"] = Review.objects.count()

		# Simple monthly enrollment chart for the current year
		now = timezone.now()
		year = now.year
		monthly_counts = (
			Enroll.objects.filter(enrolled_date__year=year)
			.extra(select={"month": "MONTH(enrolled_date)"})
			.values("month")
			.annotate(c=Count("id"))
			.order_by("month")
		)

		labels = []
		data = []
		month_map = {row["month"]: row["c"] for row in monthly_counts}
		for m in range(1, 13):
			labels.append(str(m))
			data.append(month_map.get(m, 0))

		extra_context["chart_labels"] = labels
		extra_context["chart_data"] = data

		return super().index(request, extra_context=extra_context)


admin_site = LMSAdminSite(name="lms_admin")


User = get_user_model()

admin_site.register(User)
admin_site.register(Profile)
