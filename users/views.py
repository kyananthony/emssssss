from urllib import request
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

def base(request):
    pass
    return render (request, 'base.html')

def register(request):
    pass
    return render (request, 'register.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
    if user is not None:
        login (request, user)
        return redirect('home')
    else:
        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')