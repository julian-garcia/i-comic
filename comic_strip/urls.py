from django.urls import path
from .views import comic_strip, comic_strip_add

urlpatterns = [
    path('', comic_strip, name='comic_strip'),
    path('add', comic_strip_add, name='comic_strip_add'),
]
