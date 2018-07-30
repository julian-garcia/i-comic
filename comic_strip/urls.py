from django.urls import path
from .views import comic_strip, comic_strip_add, comic_strip_frame_add

urlpatterns = [
    path('add', comic_strip_add, name='comic_strip_add'),
    path('add-frame/<id>', comic_strip_frame_add, name='comic_strip_frame_add'),
    path('<id>', comic_strip, name='comic_strip'),
]
