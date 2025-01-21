from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
import os

def sign_up(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Success !')
            return redirect('/account/login')
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)


@login_required(login_url = '/usAuth/account/login')
def log_out(request):
    logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('http://127.0.0.1:7999/account/login')


@csrf_exempt
def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # django login
            login(request, user)
            messages.success(request, 'You are now logged in.')

            return redirect("http://127.0.0.1:8000/stockapp/")
        else:
            messages.warning(request, 'Invalid login credentials')
            return redirect('/account/login' )
    
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)