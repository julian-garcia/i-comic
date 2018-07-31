from django.urls import path
from .views import ticket_listing

urlpatterns = [
    path('', ticket_listing, name='ticket_listing')
]
