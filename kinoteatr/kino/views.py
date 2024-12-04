from django.shortcuts import render, get_object_or_404
from .models import *

def index(request):
    return render(request,'index.html')
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

