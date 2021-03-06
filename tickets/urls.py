from django.urls import path
from .views import ticket_listing, ticket_view, ticket_add, ticket_edit, ticket_upvote, comment_add, update_tickets

urlpatterns = [
    path('', ticket_listing, name='ticket_listing'),
    path('add', ticket_add, name='ticket_add'),
    path('update', update_tickets, name='update_tickets'),
    path('edit/<id>', ticket_edit, name='ticket_edit'),
    path('view/<id>', ticket_view, name='ticket_view'),
    path('upvote/<id>', ticket_upvote, name='ticket_upvote'),
    path('comment/<id>', comment_add, name='comment_add'),
]
