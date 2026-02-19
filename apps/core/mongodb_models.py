"""Sample MongoDB models using mongoengine."""

from mongoengine import Document, StringField, EmailField, URLField, DateTimeField, ListField, ReferenceField, BooleanField, IntField
from datetime import datetime

class Author(Document):
    """Author document for MongoDB."""
    name = StringField(required=True, max_length=100)
    email = EmailField(unique=True)
    bio = StringField(max_length=500)
    created_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'authors',
        'indexes': ['email']
    }
    
    def __str__(self):
        return self.name


class BlogPost(Document):
    """Blog post document for MongoDB."""
    title = StringField(required=True, max_length=200)
    slug = StringField(unique=True)
    author = ReferenceField(Author, required=True)
    content = StringField(required=True)
    tags = ListField(StringField(max_length=50))
    published = BooleanField(default=False)
    views = IntField(default=0)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'blog_posts',
        'indexes': ['slug', 'author']
    }
    
    def __str__(self):
        return self.title


class CourseReview(Document):
    """Course reviews in MongoDB (optional for your e-learning project)."""
    course_id = StringField(required=True)  # Reference to Django Course
    user_email = EmailField(required=True)
    rating = IntField(min_value=1, max_value=5, required=True)
    comment = StringField(max_length=1000)
    created_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'course_reviews',
        'indexes': ['course_id', 'user_email']
    }
    
    def __str__(self):
        return f"{self.course_id} - {self.rating}⭐"
