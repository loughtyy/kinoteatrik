from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login as lo, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

def index(request):
    films = Products.objects.all()[:3]
    return render(request,'index.html', {'films':films})
def films(request):
    films = Products.objects.all()
    return render(request, 'films.html', {'films': films})
def contact(request):
    return render(request, 'contact.html')
def film_detail(request, film_id):
    film = get_object_or_404(Products, id=film_id)
    return render(request, 'film_detail.html', {'film': film})

def session_schedule(request):
    sessions = Session.objects.all()  
    return render(request, 'session_schedule.html', {'sessions': sessions})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            lo(request, user)
            return redirect('index')
        else:
            messages.error(request, "Неверные учетные данные")
    return render(request, 'login.html', {})
