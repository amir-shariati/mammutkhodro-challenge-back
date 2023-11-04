from django.conf import settings

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Portfolio API Project',
    'DESCRIPTION': 'This is API document for Portfolio App',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
