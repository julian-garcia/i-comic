from django.urls import path
from .views import ticket_listing, ticket_view, ticket_add, ticket_edit, ticket_upvote

urlpatterns = [
    path('', ticket_listing, name='ticket_listing'),
    path('add', ticket_add, name='ticket_add'),
    path('edit/<id>', ticket_edit, name='ticket_edit'),
    path('view/<id>', ticket_view, name='ticket_view'),
    path('upvote/<id>', ticket_upvote, name='ticket_upvote'),
]
