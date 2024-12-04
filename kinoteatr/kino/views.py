from django.shortcuts import render

def index(request):
    return render(request,'index.html')
def films(request):
    return render(request, 'films.html')
def contact(request):
    return render(request, 'contact.html')
