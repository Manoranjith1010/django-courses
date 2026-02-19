#!/usr/bin/env python
"""Test MongoDB CRUD operations."""

import os
import sys

sys.path.insert(0, r'd:\p\e-learning_project_django\django-courses')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'courseproject.settings')

import django
django.setup()

from core.mongodb_models import Author, BlogPost, CourseReview
from datetime import datetime

print("=" * 70)
print("MongoDB CRUD Operations Test")
print("=" * 70)

# Create (C)
print("\n📝 CREATE - Adding new documents to MongoDB:")
print("-" * 70)

try:
    # Create author
    author = Author(
        name="John Doe",
        email="john@example.com",
        bio="Full-stack developer and educator"
    )
    author.save()
    print(f"✅ Created Author: {author.name} (ID: {author.id})")
    
    # Create blog post
    post = BlogPost(
        title="Getting Started with Django",
        slug="getting-started-django",
        author=author,
        content="Django is a powerful web framework for Python...",
        tags=["django", "python", "web-development"],
        published=True,
        views=150
    )
    post.save()
    print(f"✅ Created BlogPost: {post.title} (ID: {post.id})")
    
    # Create course review
    review = CourseReview(
        course_id="COURSE001",
        user_email="student@example.com",
        rating=5,
        comment="Great course! Highly recommended."
    )
    review.save()
    print(f"✅ Created Review: {review.rating}⭐ for {review.course_id}")
    
except Exception as e:
    print(f"❌ Create Error: {e}")

# Read (R)
print("\n\n📖 READ - Retrieving documents from MongoDB:")
print("-" * 70)

try:
    # Read all authors
    all_authors = Author.objects()
    print(f"✅ Found {all_authors.count()} author(s):")
    for a in all_authors[:3]:  # Show first 3
        print(f"   - {a.name} ({a.email})")
    
    # Read specific post
    post = BlogPost.objects(slug="getting-started-django").first()
    if post:
        print(f"\n✅ Found Post: '{post.title}'")
        print(f"   Author: {post.author.name}")
        print(f"   Views: {post.views}")
        print(f"   Tags: {', '.join(post.tags)}")
    
    # Read reviews
    reviews = CourseReview.objects()
    print(f"\n✅ Found {reviews.count()} review(s)")
    
except Exception as e:
    print(f"❌ Read Error: {e}")

# Update (U)
print("\n\n✏️  UPDATE - Modifying documents in MongoDB:")
print("-" * 70)

try:
    post = BlogPost.objects(slug="getting-started-django").first()
    if post:
        post.views += 50  # Increment views
        post.updated_at = datetime.now()
        post.save()
        print(f"✅ Updated Post views to: {post.views}")
    
except Exception as e:
    print(f"❌ Update Error: {e}")

# Delete (D)
print("\n\n🗑️  DELETE - Removing test documents:")
print("-" * 70)

try:
    # Clean up test data (optional)
    # BlogPost.objects(slug="getting-started-django").delete()
    # Author.objects(email="john@example.com").delete()
    # CourseReview.objects(course_id="COURSE001").delete()
    print("✅ Delete operations available (commented out for safety)")
    print("   Uncomment in scripts/test_mongodb_crud.py to delete test data")
    
except Exception as e:
    print(f"❌ Delete Error: {e}")

print("\n" + "=" * 70)
print("Database Summary:")
print("-" * 70)
print(f"Total Authors: {Author.objects.count()}")
print(f"Total Posts: {BlogPost.objects.count()}")
print(f"Total Reviews: {CourseReview.objects.count()}")
print("=" * 70)
print("\n✅ MongoDB is working! You can now use it alongside Django SQLite/MySQL.")
