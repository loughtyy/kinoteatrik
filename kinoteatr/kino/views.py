from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login as lo, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework import viewsets
from .models import *
from rest_framework import status
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Products
from .serializers import ProductSerializer

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

class BuyTicketsPageView(View):
      def get(self, request, film_id):
        film = get_object_or_404(Products, id=film_id)
        sessions = Session.objects.filter(film=film)  # Получаем сеансы для данного фильма
        form = TicketForm() 
        return render(request, 'buy_tickets.html', {
            'film': film,
            'form': form,
            'sessions': sessions  # Передаем сеансы в контекст
        })

      def post(self, request, film_id):
        film = get_object_or_404(Products, id=film_id)
        form = TicketForm(request.POST) 

        if form.is_valid():
            # Сохранение билета
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.session = form.cleaned_data['session']
            ticket.save()

            request.session['selected_film_id'] = film_id  # Устанавливаем ID фильма в сессии
            return redirect('success_page')
        else:
            # Если форма некорректна, показываем ошибки
            sessions = Session.objects.filter(film=film)  # Получаем сеансы для данного фильма
            return render(request, 'buy_tickets.html', {
                'film': film,
                'form': form,
                'sessions': sessions  # Передаем сеансы в контекст
            })
class TicketsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            tickets = Ticket.objects.filter(user=request.user) 
            return render(request, 'tickets.html', {'tickets': tickets})
        else:
            return redirect('login') 
 
def success_view(request):
    film_id = request.session.get('selected_film_id')
    if not film_id:
        return redirect('index') 

    film = get_object_or_404(Products, id=film_id)
    return render(request, 'success.html', {'film': film})

from django import forms
class TicketForm(forms.ModelForm):
    session = forms.ModelChoiceField(queryset=Session.objects.all(), required=True)

    class Meta:
        model = Ticket
        fields = ['session']

class ProductsViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Products.objects.all()
    
    
from rest_framework.generics import RetrieveUpdateAPIView
class SingleProductView(RetrieveUpdateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer


    