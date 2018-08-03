from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User

class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email', 'password']

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']
