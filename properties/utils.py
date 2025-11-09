from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Check if the queryset exists in Redis
    properties = cache.get('all_properties')

    if not properties:
        # Fetch from database if not cached
        properties = list(Property.objects.all())
        # Cache for 1 hour (3600 seconds)
        cache.set('all_properties', properties, timeout=3600)

    return properties
