from django.urls import path
from .views import view_cart, adjust_cart, adjust_upvote_cart

urlpatterns = [
    path('', view_cart, name='view_cart'),
    path('adjust-cart/<title>', adjust_cart, name='adjust_cart'),
    path('adjust-upvote-cart/<id>', adjust_upvote_cart, name='adjust_upvote_cart'),
]
