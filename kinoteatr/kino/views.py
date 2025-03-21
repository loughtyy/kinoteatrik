from django.contrib.auth import login as lo, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework import viewsets, permissions
from .permissions import IsOwnerOrReadOnly
from .models import *
from django.views import View
from .serializers import *
from django.contrib.auth.models import User

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
            # Сохранение билета
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
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


class SessionViewSet(viewsets.ModelViewSet):
    serializer_class = SessionSerializer
    queryset = Session.objects.all()
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
    'users': reverse('user-list', request=request, format=format),
    'products': reverse('product-list', request=request, format=format)
    })

from rest_framework import generics
from rest_framework import renderers
from rest_framework.response import Response
from .models import Products
from .serializers import ProductSerializer  

class ProductsHighlight(generics.GenericAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer  
    def get(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product) 
        return Response(serializer.data)
    
class SessionHighlight(generics.GenericAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer 

    def get(self, request, *args, **kwargs):
        session = self.get_object()
        serializer = self.get_serializer(session)  
        return Response(serializer.data) 

class TicketHighlight(generics.GenericAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer 

    def get(self, request, *args, **kwargs):
        ticket = self.get_object()
        serializer = self.get_serializer(ticket)  
        return Response(serializer.data)  

class UserHighlight(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer 

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)  
        return Response(serializer.data)  