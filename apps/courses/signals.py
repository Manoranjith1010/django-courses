"""
Cache-invalidation signals for the courses app.

When a Topic is created, updated, or deleted the head_menu context
processor cache entry is cleared so the navigation menu reflects the
change on the next request.
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import Topic


@receiver([post_save, post_delete], sender=Topic)
def clear_topic_cache(sender, **kwargs):
    """Invalidate the cached topic list used by the nav menu."""
    cache.delete('head_menu_topics')
