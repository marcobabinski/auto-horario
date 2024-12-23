from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.backends import UserModel
from django.shortcuts import render, redirect, get_object_or_404
from autohorario.forms import FormLogin
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .forms import TurmaForm, ProfissionalForm, AtividadeForm
from .models import Profile 
from django.contrib.auth.decorators import login_required

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

from autohorario.models import Profissional, Turma, Atividade

@login_required
def profissionais(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None 

    if request.GET.get('new'):
        if request.method == "POST":
            form = ProfissionalForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('profissionais') 
        else:
            form = ProfissionalForm()

        return render(request, "create_profissional.html", {'form': form, 'profile': profile})

    profissionais = Profissional.objects.all().order_by("nome")
    form = {profissional.pk: ProfissionalForm(instance=profissional) for profissional in profissionais}

    return render(request, "profissionais.html", {'profissionais': profissionais, 'sidebar': 'profissionais', 'profile': profile, 'form': form })

@login_required
def agenda(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None 

    profissionais = Profissional.objects.all()
    return render(request, "agenda.html", {'profissionais': profissionais, 'sidebar': 'agenda', 'profile': profile})

@login_required
def turmas(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None 

    if request.GET.get('new'):
        if request.method == "POST":
            form = TurmaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('turmas') 
        else:
            form = TurmaForm()

        return render(request, "create_turma.html", {'form': form, 'profile': profile})

    turmas = Turma.objects.all().order_by("nome")
    form = {turma.pk: TurmaForm(instance=turma) for turma in turmas}
    
    # Caso contrário, renderiza a lista geral de turmas.
    return render(request, "turmas.html", {'turmas': turmas, 'profile': profile, 'sidebar': 'turmas'})

@login_required
def vinculos(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None 
    profissionais = Profissional.objects.all()
    return render(request, "vinculos.html", {'profissionais': profissionais, 'profile': profile, 'sidebar': 'vínculos'})

@login_required
def atividades(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None 

    if request.GET.get('new'):
        if request.method == "POST":
            form = AtividadeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('atividades') 
        else:
            form = AtividadeForm()

        return render(request, "create_atividade.html", {'form': form, 'profile': profile})

    atividades = Atividade.objects.select_related('id_caracteristica').all().order_by("nome")
    
    return render(request, "atividades.html", {'atividades': atividades, 'profile': profile, 'sidebar': 'atividades'})

@login_required
def delete_atividade(request, id_atividade):
    atividade = get_object_or_404(Atividade, id_atividade=id_atividade)

    if request.method == "POST":
        atividade.delete()
    
    return redirect('atividades')

@login_required
def edit_atividade(request, id_atividade):
    atividade = get_object_or_404(Atividade, id_atividade=id_atividade)

    if request.method == "POST":
        form = AtividadeForm(request.POST, instance=atividade)
        if form.is_valid():
            form.save()
            return redirect('atividades')
    
    return redirect('atividades')

@login_required
def delete_turma(request, id_turma):
    turma = get_object_or_404(Turma, id_turma=id_turma)

    if request.method == "POST":
        turma.delete()
    
    return redirect('turmas')

@login_required
def edit_turma(request, id_turma):
    turma = get_object_or_404(Turma, id_turma=id_turma)

    if request.method == "POST":
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            return redirect('turmas')
    
    return redirect('turmas')

@login_required
def delete_profissional(request, id_profissional):
    profissional = get_object_or_404(Profissional, id_profissional=id_profissional)

    if request.method == "POST":
        profissional.delete()
    
    return redirect('profissionais')

@login_required
def edit_profissional(request, id_profissional):
    profissional = get_object_or_404(Profissional, id_profissional=id_profissional)

    if request.method == "POST":
        form = ProfissionalForm(request.POST, instance=profissional)
        if form.is_valid():
            form.save()
            return redirect('profissionais')
    
    return redirect('profissionais')

def teste(request):
    if request.method == "POST":
        print("POOOOST")
    else:
        print("ÃAAAAAN")
    return HttpResponse("a")

@login_required
def export(request):
    data = {}

    turmas = list(Turma.objects.values())
    profissionais = list(Profissional.objects.values())
    atividades = list(Atividade.objects.values())

    data["turmas"] = turmas
    data["profissionais"] = profissionais
    data["atividades"] = atividades

    return JsonResponse(data, safe=False)