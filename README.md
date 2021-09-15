# Required Settings 
## Create file: /etc/django-conf-files/accesspointlocator.json

The json file needs to contain the following parameters:
- DEBUG: <true/False> (Determines Prod/Dev)
- ALLOWED_HOSTS: *
- SECRET_KEY: django-secret-key
- GEOLOCATION_KEY: Google API key

These parameters are needed by the django.conf.settings file
