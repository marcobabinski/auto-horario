from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    nome = "Gustavo Lima"
    return HttpResponse(f"Olár {nome}")

def base(request):
    return render(request, "base.html")

def recoverPassword(request):
    return render(request, "password-recovery.html")