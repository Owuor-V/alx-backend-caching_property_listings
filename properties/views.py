from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .utils import get_all_properties

@cache_page(60 * 15)  # Cache HTML response for 15 minutes
def property_list(request):
    properties = get_all_properties()  # Uses Redis low-level cache
    return render(request, "properties/property_list.html", {"properties": properties})
