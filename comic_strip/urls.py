from django.urls import path
from .views import comic_strip_listing

urlpatterns = [
    path('', comic_strip_listing, name='comic_strip_listing'),
]
