from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.backends import UserModel
from django.shortcuts import render, redirect, get_object_or_404
from autohorario.forms import FormLogin
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .forms import TurmaForm
from .models import Profile

def index(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    else:
        return redirect(fazer_login)

def fazer_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/agenda")

    if request.method == 'POST':
        form = FormLogin(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            senha = form.cleaned_data['senha']
            user = authenticate(request, username=usuario, password=senha) # retorna None se o usuário não é válido
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/agenda")
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

from autohorario.models import Profissional, Turma

def profissionais(request):
    profissionais = Profissional.objects.all()
    return render(request, "profissionais.html", {'profissionais': profissionais})

def agenda(request):
    profissionais = Profissional.objects.all()
    return render(request, "agenda.html", {'profissionais': profissionais})

def turmas(request):
    # Verifica se o usuário está autenticado
    if request.user.is_authenticated:
        # Acessa o perfil vinculado ao usuário autenticado
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None  # Caso o perfil ainda não tenha sido criado
    
    # Verifica se há um parâmetro "edit_id" na requisição.
    edit_id = request.GET.get('edit_id')

    if edit_id:
        # Tenta buscar a turma correspondente; se não existir, retorna 404.
        turma = get_object_or_404(Turma, id_turma=edit_id)

        # Cria um formulário pré-preenchido com os dados da turma.
        if request.method == "POST":
            form = TurmaForm(request.POST, instance=turma)
            if form.is_valid():
                form.save()
                return redirect('turmas')  # Redireciona para a página geral de turmas.
        else:
            form = TurmaForm(instance=turma)
        
        return render(request, "turmas.html", {'form': form, 'turma': turma})
    
    # Verifica se há um parâmetro "delete_id" na requisição.
    delete_id = request.GET.get('delete_id')

    if delete_id:
        # Tenta buscar a turma correspondente; se não existir, retorna 404.
        turma = get_object_or_404(Turma, id_turma=delete_id)

        # Apaga a turma.
        if request.method == "POST":
            turma.delete()
            return redirect('turmas')  # Redireciona para a página geral de turmas.

        # Renderiza a confirmação de exclusão.
        return render(request, "delete_turma.html", {'turma': turma})

    # Verifica se o parâmetro "new" está presente na requisição para criação de uma nova turma.
    if request.GET.get('new'):
        if request.method == "POST":
            form = TurmaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('turmas')  # Redireciona para a página geral de turmas.
        else:
            form = TurmaForm()

        # Renderiza o formulário de criação.
        return render(request, "create_turma.html", {'form': form})
    
    # Caso contrário, renderiza a lista geral de turmas.
    turmas = Turma.objects.all()
    return render(request, "turmas.html", {'turmas': turmas, 'profile': profile})

def vinculos(request):
    profissionais = Profissional.objects.all()
    return render(request, "vinculos.html", {'profissionais': profissionais})

def atividades(request):
    profissionais = Profissional.objects.all()
    return render(request, "atividades.html", {'profissionais': profissionais})
