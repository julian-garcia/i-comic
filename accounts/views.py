from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from accounts.forms import UserLoginForm, UserRegistrationForm
from accounts.models import User
from django.contrib import auth, messages

def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method=='POST':
        login_form = UserLoginForm(request.POST)
        user = auth.authenticate(username=request.POST['email'],
                                 password=request.POST['password'])
        if user:
            auth.login(user=user,request=request)
            messages.success(request, 'Logged in')
            return redirect(reverse('index'))
        else:
            login_form.add_error(None, "User name or password incorrect")
    else:
        login_form = UserLoginForm()

    return render(request, 'login.html', {'login_form': login_form})

def registration(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method=='POST':
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            user = auth.authenticate(username=request.POST['email'],
                                     password=request.POST['password1'])
            if user:
                auth.login(user=user,request=request)
                messages.success(request, 'You have been registered')
                return redirect(reverse('index'))
            else:
                messages.error(request, 'Unable to register your account')
    else:
        registration_form = UserRegistrationForm()

    return render(request, 'register.html', {'registration_form': registration_form})

@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out')
    return redirect(reverse('index'))
