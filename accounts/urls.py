from django.urls import path
from .views import login, registration, logout

urlpatterns = [
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('register', registration, name='register'),
]
