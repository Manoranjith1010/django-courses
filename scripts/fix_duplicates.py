"""
Django Migration Fix Script - Remove Duplicates Before Applying Unique Constraints

This script identifies and removes duplicate records that would violate unique_together
constraints on Enroll, LectureProgress, and Review models.

Usage:
    python manage.py shell < scripts/fix_duplicates.py
    
Or run interactively:
    python manage.py shell
    >>> exec(open('scripts/fix_duplicates.py').read())

CAUTION: This script DELETES data. Only run in development or after backing up production data.
"""

from django.db.models import Count, Min
from courses.models import Enroll, Lecture

print("=" * 60)
print("DJANGO DUPLICATE RECORD FIXER")
print("=" * 60)


# =============================================================================
# 1. FIX ENROLL DUPLICATES (user + course must be unique)
# =============================================================================
print("\n[1] Checking Enroll model for duplicates...")

# Find duplicates: same user enrolled in same course multiple times
enroll_duplicates = (
    Enroll.objects
    .values('user', 'course')
    .annotate(count=Count('id'), min_id=Min('id'))
    .filter(count__gt=1)
)

if enroll_duplicates.exists():
    duplicate_count = enroll_duplicates.count()
    print(f"    Found {duplicate_count} duplicate user-course combinations")
    
    total_deleted = 0
    for dup in enroll_duplicates:
        # Keep the oldest record (min_id), delete the rest
        deleted, _ = Enroll.objects.filter(
            user_id=dup['user'],
            course_id=dup['course']
        ).exclude(id=dup['min_id']).delete()
        total_deleted += deleted
    
    print(f"    ✓ Deleted {total_deleted} duplicate Enroll records")
else:
    print("    ✓ No duplicates found in Enroll")


# =============================================================================
# 2. FIX LECTUREPROGRESS DUPLICATES (user + lecture must be unique)
# =============================================================================
print("\n[2] Checking LectureProgress model for duplicates...")

try:
    from courses.models import LectureProgress
    
    progress_duplicates = (
        LectureProgress.objects
        .values('user', 'lecture')
        .annotate(count=Count('id'), min_id=Min('id'))
        .filter(count__gt=1)
    )
    
    if progress_duplicates.exists():
        duplicate_count = progress_duplicates.count()
        print(f"    Found {duplicate_count} duplicate user-lecture combinations")
        
        total_deleted = 0
        for dup in progress_duplicates:
            deleted, _ = LectureProgress.objects.filter(
                user_id=dup['user'],
                lecture_id=dup['lecture']
            ).exclude(id=dup['min_id']).delete()
            total_deleted += deleted
        
        print(f"    ✓ Deleted {total_deleted} duplicate LectureProgress records")
    else:
        print("    ✓ No duplicates found in LectureProgress")
        
except Exception as e:
    print(f"    ⚠ LectureProgress table may not exist yet: {e}")


# =============================================================================
# 3. FIX REVIEW DUPLICATES (user + course must be unique)
# =============================================================================
print("\n[3] Checking Review model for duplicates...")

try:
    from courses.models import Review
    
    review_duplicates = (
        Review.objects
        .values('user', 'course')
        .annotate(count=Count('id'), min_id=Min('id'))
        .filter(count__gt=1)
    )
    
    if review_duplicates.exists():
        duplicate_count = review_duplicates.count()
        print(f"    Found {duplicate_count} duplicate user-course reviews")
        
        total_deleted = 0
        for dup in review_duplicates:
            deleted, _ = Review.objects.filter(
                user_id=dup['user'],
                course_id=dup['course']
            ).exclude(id=dup['min_id']).delete()
            total_deleted += deleted
        
        print(f"    ✓ Deleted {total_deleted} duplicate Review records")
    else:
        print("    ✓ No duplicates found in Review")
        
except Exception as e:
    print(f"    ⚠ Review table may not exist yet: {e}")


# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 60)
print("CLEANUP COMPLETE")
print("=" * 60)
print("\nNext steps:")
print("  1. Exit the shell: exit()")
print("  2. Run migration: python manage.py migrate")
print("  3. If errors persist, check for more duplicates manually")
print("")
