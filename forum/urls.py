from django.urls import path
from .views import forum, add_topic, view_topic, add_comment

urlpatterns = [
    path('', forum, name='forum'),
    path('add-topic', add_topic, name='add_topic'),
    path('view/<id>', view_topic, name='view_topic'),
    path('comment/<id>', add_comment, name='add_comment'),
]
