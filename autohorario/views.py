from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.backends import UserModel
from django.shortcuts import render
from autohorario.forms import FormLogin
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return HttpResponseRedirect("/login/")


def testecomponents(request):
    return render(request, "components/menu.html")

def testecomponents2(request):
    return render(request, "components/cards.html")

def fazer_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")

    if request.method == 'POST':
        form = FormLogin(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            senha = form.cleaned_data['senha']
            user = authenticate(request, username=usuario, password=senha) # retorna None se o usuário não é válido
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                messages.error(request, "Usuário e/ou senha incorretos. Tente de novo.")
        else:
            messages.error(request, "Preencha corretamente o formulário")

    else:
        form = FormLogin()

    contexto = {"form": form}
    return render(request, 'login.html', contexto)

def fazer_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

def recoverPassword(request):
    return render(request, "password-recovery.html")