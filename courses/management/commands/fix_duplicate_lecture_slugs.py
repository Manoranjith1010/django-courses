from django.core.management.base import BaseCommand
from django.db import models, transaction

from courses.models import Lecture


class Command(BaseCommand):
    help = "Fix duplicate lecture slugs per course by appending a numeric suffix."

    def add_arguments(self, parser):
        parser.add_argument(
            "--course-id",
            type=int,
            dest="course_id",
            help="Only fix duplicates for a specific course id.",
        )
        parser.add_argument(
            "--slug",
            type=str,
            dest="lecture_slug",
            help="Only fix duplicates for a specific lecture slug.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show changes without saving.",
        )

    def handle(self, *args, **options):
        course_id = options.get("course_id")
        lecture_slug = options.get("lecture_slug")
        dry_run = options.get("dry_run")

        dupes = (
            Lecture.objects.values("course_id", "lecture_slug")
            .annotate(cnt=models.Count("id"))
            .filter(cnt__gt=1)
        )
        if course_id is not None:
            dupes = dupes.filter(course_id=course_id)
        if lecture_slug:
            dupes = dupes.filter(lecture_slug=lecture_slug)

        if not dupes.exists():
            self.stdout.write(self.style.SUCCESS("No duplicate lecture slugs found."))
            return

        with transaction.atomic():
            for group in dupes:
                course_id = group["course_id"]
                base_slug = group["lecture_slug"]
                lectures = (
                    Lecture.objects.filter(course_id=course_id, lecture_slug=base_slug)
                    .order_by("id")
                )
                if lectures.count() < 2:
                    continue

                existing_slugs = set(
                    Lecture.objects.filter(course_id=course_id).values_list(
                        "lecture_slug", flat=True
                    )
                )

                for index, lecture in enumerate(lectures):
                    if index == 0:
                        continue

                    suffix = 2
                    while True:
                        new_slug = f"{base_slug}-{suffix}"
                        if new_slug not in existing_slugs:
                            break
                        suffix += 1

                    msg = (
                        f"course_id={course_id} lecture_id={lecture.id} "
                        f"{lecture.lecture_slug} -> {new_slug}"
                    )
                    if dry_run:
                        self.stdout.write(f"DRY RUN: {msg}")
                    else:
                        lecture.lecture_slug = new_slug
                        lecture.save(update_fields=["lecture_slug"])
                        self.stdout.write(self.style.SUCCESS(msg))

                    existing_slugs.add(new_slug)

            if dry_run:
                self.stdout.write(self.style.WARNING("Dry run complete. No changes saved."))
