"""
Data Migration: Convert Yes/No CharField values to Boolean

This script converts existing 'Yes'/'No' string values to True/False
for the following fields:
- Topic.topic_is_active
- Course.course_is_active
- Course.course_is_featured
- Lecture.lecture_previewable

Run this BEFORE applying the schema migration that changes field types.

Usage:
    python manage.py shell < scripts/convert_yes_no_to_bool.py
"""

from django.db import connection


def convert_yes_no_to_boolean():
    """
    SQL script to convert 'Yes'/'No' values to 1/0 before schema migration.
    Run this if you have existing data in the database.
    """
    
    with connection.cursor() as cursor:
        # Convert Topic.topic_is_active
        print("Converting Topic.topic_is_active...")
        cursor.execute("""
            UPDATE courses_topic 
            SET topic_is_active = CASE 
                WHEN topic_is_active = 'Yes' THEN 1 
                ELSE 0 
            END
        """)
        print(f"  Updated {cursor.rowcount} rows")
        
        # Convert Course.course_is_active
        print("Converting Course.course_is_active...")
        cursor.execute("""
            UPDATE courses_course 
            SET course_is_active = CASE 
                WHEN course_is_active = 'Yes' THEN 1 
                ELSE 0 
            END
        """)
        print(f"  Updated {cursor.rowcount} rows")
        
        # Convert Course.course_is_featured
        print("Converting Course.course_is_featured...")
        cursor.execute("""
            UPDATE courses_course 
            SET course_is_featured = CASE 
                WHEN course_is_featured = 'Yes' THEN 1 
                ELSE 0 
            END
        """)
        print(f"  Updated {cursor.rowcount} rows")
        
        # Convert Lecture.lecture_previewable
        print("Converting Lecture.lecture_previewable...")
        cursor.execute("""
            UPDATE courses_lecture 
            SET lecture_previewable = CASE 
                WHEN lecture_previewable = 'Yes' THEN 1 
                ELSE 0 
            END
        """)
        print(f"  Updated {cursor.rowcount} rows")
    
    print("\nData conversion complete!")
    print("Now run: python manage.py makemigrations courses && python manage.py migrate")


if __name__ == '__main__':
    import django
    django.setup()
    convert_yes_no_to_boolean()
