from django.urls import path
from .views import productivity

urlpatterns = [
    path('', productivity, name='productivity'),
]
