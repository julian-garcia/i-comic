from django.urls import path
from .views import view_documentation

urlpatterns = [
    path('', view_documentation, name='view_documentation'),
]
