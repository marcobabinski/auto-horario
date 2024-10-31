from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    nome = "Gusvn "
    return HttpResponse(f"Olár {nome}")

def testecomponents(request):
    return render(request, "components/menu.html")

def testecomponents2(request):
    return render(request, "components/cards.html")

def base(request):
    return render(request, "base.html")

def recoverPassword(request):
    return render(request, "password-recovery.html")