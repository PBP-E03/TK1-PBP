from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
import datetime

def user_login(request):
    # Redirect authenticated users to the main page
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:main_page'))
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:main_page"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'authentication/login.html', context)

def user_register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('authentication:user_login')
        else:
            messages.error(request, 'Error creating your account')
    context = {'form': form}
    return render(request, 'authentication/register.html', context)

def user_logout(request):
    logout(request)
    response = HttpResponseRedirect(reverse('authentication:user_login'))
    response.delete_cookie('last_login')
    return response