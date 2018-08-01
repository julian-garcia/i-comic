from django.urls import path
from .views import ticket_listing, ticket_view, ticket_add

urlpatterns = [
    path('', ticket_listing, name='ticket_listing'),
    path('add', ticket_add, name='ticket_add'),
    path('<id>', ticket_view, name='ticket_view'),
]
