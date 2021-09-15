from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import (ap_location)

urlpatterns = [
    path('get-location/', ap_location),
]

urlpatterns = format_suffix_patterns(urlpatterns)