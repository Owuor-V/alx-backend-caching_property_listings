from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    # Check if the queryset exists in Redis
    properties = cache.get('all_properties')

    if not properties:
        # Fetch from database if not cached
        properties = list(Property.objects.all())
        # Cache for 1 hour (3600 seconds)
        cache.set('all_properties', properties, timeout=3600)

    return properties

def get_redis_cache_metrics():
    # Connect to Redis using django-redis
    connection = get_redis_connection("default")
    info = connection.info("stats")

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)

    total = hits + misses
    hit_ratio = (hits / total) if total > 0 else 0

    metrics = {
        "cache_hits": hits,
        "cache_misses": misses,
        "hit_ratio": round(hit_ratio, 4)
    }

    # Log the metrics for debugging
    logger.info(f"Redis Cache Metrics: {metrics}")

    return metrics
