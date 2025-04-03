from django.contrib.auth import login as lo, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework import viewsets, permissions, generics
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, AdminRenderer
from .permissions import IsOwnerOrReadOnly
from .models import *
from django.views import View
from .serializers import *
from django.contrib.auth.models import User
from django.urls import reverse  
from rest_framework.decorators import api_view
from rest_framework.response import Response

def index(request):
    films = Products.objects.all()[:3]
    return render(request, 'index.html', {'films': films})

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

def registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Пользователь с таким именем уже существует.")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password, email=email)

        lo(request, user)

        return redirect('index')

    return render(request, 'register.html', {})

class BuyTicketsPageView(View):
    def get(self, request, film_id):
        film = get_object_or_404(Products, id=film_id)
        sessions = Session.objects.filter(film=film)
        form = TicketForm()
        return render(request, 'buy_tickets.html', {
            'film': film,
            'form': form,
            'sessions': sessions
        })

    def post(self, request, film_id):
        film = get_object_or_404(Products, id=film_id)
        form = TicketForm(request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.session = form.cleaned_data['session']
            ticket.save()

            request.session['selected_film_id'] = film_id
            return redirect('success_page')
        else:
            sessions = Session.objects.filter(film=film)
            return render(request, 'buy_tickets.html', {
                'film': film,
                'form': form,
                'sessions': sessions
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, AdminRenderer]

    def perform_create(self, serializer):
        serializer.save()

class SessionViewSet(viewsets.ModelViewSet):
    serializer_class = SessionSerializer
    queryset = Session.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, AdminRenderer]

    def perform_create(self, serializer):
        serializer.save()

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, AdminRenderer]

    def perform_create(self, serializer):
        serializer.save()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, AdminRenderer]

    def perform_create(self, serializer):
        serializer.save()

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'products': reverse('products-list', request=request, format=format),
        'sessions': reverse('sessions-list', request=request, format=format),
        'tickets': reverse('tickets-list', request=request, format=format),
        'users': reverse('users-list', request=request, format=format),
    })

