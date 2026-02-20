from django.core.cache import cache
from .models import Topic, Course, Enroll


def head_menu(request):
    """
    Provide active topics for the navigation menu.
    Optimized with .only() to fetch minimal data and cache for performance.
    """
    # Cache key for active topics (runs on every request so caching is crucial)
    cache_key = 'head_menu_topics'
    topics = cache.get(cache_key)
    
    if topics is None:
        # Fetch only required fields for the menu
        topics = list(
            Topic.objects
            .filter(topic_is_active=True)
            .only('id', 'topic_title', 'topic_slug')
            .order_by('topic_title')
        )
        # Cache for 5 minutes (300 seconds)
        cache.set(cache_key, topics, 300)
    
    return {'topics': topics}


def my_courses(request):
    """
    Provide user's recently enrolled courses for the sidebar.
    Optimized with select_related and only() for minimal queries.
    """
    if request.user.is_authenticated:
        enrolled_courses = (
            Enroll.objects
            .filter(user=request.user)
            .select_related('course')
            .only(
                'id', 'enrolled_date',
                'course__id', 'course__course_title', 'course__course_slug'
            )
            .order_by('-enrolled_date')[:5]
        )
    else:
        enrolled_courses = None
    
    return {'enrolled_courses': enrolled_courses}
