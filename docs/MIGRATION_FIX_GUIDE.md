# Django Migration & Unique Constraint Error Resolution Guide

## Problem Identification

### Error Example
```
django.db.utils.IntegrityError: (1062, "Duplicate entry '2-1' for key 'courses_enroll_user_id_course_id_abc123_uniq'")
```

### Cause
This error occurs when:
1. A `unique_together` constraint is added to a model
2. Existing data in the database already violates this constraint (duplicate records exist)
3. The migration tries to create a unique index, but the database rejects it

In your case, the `Enroll` model now has:
```python
class Meta:
    unique_together = ('user', 'course')
```

This means the same user cannot enroll in the same course twice. The error `'2-1'` indicates user_id=2 has multiple enrollments in course_id=1.

---

## Solution Options

### Option 1: Fix Duplicates (Recommended for Production)

**Step 1: Open Django Shell**
```bash
python manage.py shell
```

**Step 2: Find and Remove Duplicates**
```python
from django.db.models import Count, Min
from courses.models import Enroll

# Find duplicates
duplicates = (
    Enroll.objects
    .values('user', 'course')
    .annotate(count=Count('id'), min_id=Min('id'))
    .filter(count__gt=1)
)

# View them first (optional)
for d in duplicates:
    print(f"User {d['user']} + Course {d['course']}: {d['count']} records")

# Remove duplicates, keeping the oldest record
for dup in duplicates:
    Enroll.objects.filter(
        user_id=dup['user'],
        course_id=dup['course']
    ).exclude(id=dup['min_id']).delete()

print("Duplicates removed!")
```

**Step 3: Exit and Migrate**
```bash
exit()
python manage.py migrate
```

### Option 2: Use the Fix Script
```bash
python manage.py shell < scripts/fix_duplicates.py
python manage.py migrate
```

### Option 3: Fresh Database (Development Only)

⚠️ **WARNING: This deletes ALL data**

```bash
# For MySQL
mysql -u root -p -e "DROP DATABASE your_db_name; CREATE DATABASE your_db_name;"

# For SQLite
del db.sqlite3

# Then recreate tables
python manage.py migrate
python manage.py createsuperuser
```

---

## Best Practices to Avoid This Issue

### 1. Add Constraints to New Models from the Start
```python
class Enroll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'course')  # Add immediately
```

### 2. Clean Data Before Adding Constraints
Before adding `unique_together` to existing models:
```python
# In a data migration or management command
from django.db.models import Count, Min

duplicates = Model.objects.values('field1', 'field2').annotate(
    count=Count('id'), 
    min_id=Min('id')
).filter(count__gt=1)

for dup in duplicates:
    Model.objects.filter(
        field1=dup['field1'],
        field2=dup['field2']
    ).exclude(id=dup['min_id']).delete()
```

### 3. Use get_or_create / update_or_create
```python
# Instead of:
Enroll.objects.create(user=user, course=course)

# Use:
enrollment, created = Enroll.objects.get_or_create(
    user=user,
    course=course,
    defaults={'enrolled_date': timezone.now()}
)
```

### 4. Validate in Views Before Creating
```python
def enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if Enroll.objects.filter(user=request.user, course=course).exists():
        messages.error(request, "Already enrolled in this course.")
        return redirect('course-detail', course_slug=course.course_slug)
    
    Enroll.objects.create(user=request.user, course=course)
```

---

## Interview-Level Explanation

**Q: Why do unique constraint migrations fail?**

**A:** Unique constraints fail when existing data violates the uniqueness rule being enforced. When we add `unique_together = ('user', 'course')`, the database attempts to create a composite unique index on those columns. If any two rows share the same combination of values (e.g., user_id=2, course_id=1 appearing twice), the index creation fails with an IntegrityError.

**Key points:**
1. The database enforces constraints at write time, but creating an index requires scanning existing data
2. The migration is atomic - if the constraint can't be applied, the entire migration fails
3. Solution: Clean data first (remove duplicates), then apply the migration
4. Prevention: Add constraints when creating models, or use data migrations to clean before adding constraints

**For new developers:**
Think of it like adding a "no duplicate names" rule to a class roster that already has two students named "John Smith" - you must resolve the duplicates before the rule can be enforced.

---

## django-allauth Settings Update

If you see this warning:
```
WARNINGS: 
account.W001: ACCOUNT_EMAIL_VERIFICATION is deprecated.
```

Add to your `settings.py`:
```python
# Updated allauth settings (version 0.50+)
ACCOUNT_EMAIL_VERIFICATION = "optional"  # or "mandatory" / "none"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True

# Disable deprecated warning
SILENCED_SYSTEM_CHECKS = ['account.W001']  # Only if needed
```

---

## Quick Reference Commands

```bash
# Check current migration status
python manage.py showmigrations

# Create new migration after model changes
python manage.py makemigrations

# Apply all pending migrations
python manage.py migrate

# Roll back to a specific migration (use with caution)
python manage.py migrate courses 0005_previous_migration

# Fake a migration (mark as applied without running)
python manage.py migrate courses 0006_new_migration --fake

# Check for issues without making changes
python manage.py check
```
