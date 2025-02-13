from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.backends import UserModel
from django.shortcuts import render, redirect, get_object_or_404
from autohorario.forms import FormLogin
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .forms import TurmaForm, ProfissionalForm, AtividadeForm, VinculoForm
from .models import Profile, VinculoProfissionalAtividade
from django.contrib.auth.decorators import login_required
import os
from oi import run
import threading

import json
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

import datetime

def salvar_matriz(matriz):
    matriz_convertida = []
    
    for periodo in matriz:
        periodo_convertido = []
        for prof_id, turma_id in periodo:
            prof = Profissional.objects.get(id_profissional=prof_id).nome if Profissional.objects.filter(id_profissional=prof_id).exists() else "Desconhecido"
            turma = Turma.objects.get(id_turma=turma_id).nome if Turma.objects.filter(id_turma=turma_id).exists() else "Desconhecido"
            periodo_convertido.append([prof, turma])
        matriz_convertida.append(periodo_convertido)
    
    with open("matriz_periodos.json", "w") as f:
        json.dump(matriz_convertida, f)

def carregar_arquivo(caminho):
    with open(caminho, "r") as f:
        return json.load(f)
    
def carregar_timestamp():
    try:
        with open("oi-tstamp.txt", "r") as f:
            timestamp_str = f.read().strip()  # Remove espaços extras
            dt_obj = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")  # Converte para datetime
            return dt_obj
    except (FileNotFoundError, ValueError):
        return None  # Retorna None em caso de erro

def index(request):
    if request.user.is_authenticated:
        return redirect(dashboard)
    else:
        return redirect(fazer_login)

@login_required
def dashboard(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None 
    return render(request, 'dashboard.html', {'profile': profile})

def fazer_login(request):
    if request.user.is_authenticated:
        return agenda(request)

    if request.method == 'POST':
        form = FormLogin(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            senha = form.cleaned_data['senha']
            user = authenticate(request, username=usuario, password=senha) # retorna None se o usuário não é válido
            if user is not None:
                login(request, user)
                return agenda(request)
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
    messages.info(request, "Deslogado com sucesso")
    return index(request)

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

    # if request.GET.get('new'):
    #     if request.method == "POST":
    #         form = ProfissionalForm(request.POST)
    #         if form.is_valid():
    #             form.save()
    #             return redirect('profissionais') 
    #     else:
    #         form = ProfissionalForm()

        # return render(request, "create_profissional.html", {'form': form, 'profile': profile})

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

    # Exemplo da matriz convertida
    matriz = carregar_arquivo("matriz_periodos.json")

    p1 = matriz[0::4]
    p2 = matriz[1::4]
    p3 = matriz[2::4]
    p4 = matriz[3::4]

    periodos = [p1,p2,[],p3,p4]

    # Mapeia os horários para os índices da matriz
    horarios = [
        "7:45 - 8:45", "8:45 - 9:30", "9:30 - 10:00", "10:00 - 10:45", "10:45 - 11:30",
    ]

    cores = [
        'red', 'orange', 'yellow', 'green', 'blue',     
    ]
    
    # Lista de dias da semana
    dias = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']

    dt_obj = carregar_timestamp()
    data_legivel = dt_obj.strftime("%d de %B de %Y, %H:%M") if dt_obj else "Sem dados" if dt_obj else "Sem dados"

    # Para traduzir o nome do mês para português corretamente
    meses = {
        "January": "Janeiro", "February": "Fevereiro", "March": "Março", "April": "Abril",
        "May": "Maio", "June": "Junho", "July": "Julho", "August": "Agosto",
        "September": "Setembro", "October": "Outubro", "November": "Novembro", "December": "Dezembro"
    }
    for en, pt in meses.items():
        data_legivel = data_legivel.replace(en, pt)

    contexto = {
        "horarios": horarios,
        # "matriz_convertida": matriz,
        "gen_date": data_legivel,  # Pode ser preenchido com a data de exportação
        "full_name": request.user.get_full_name() if request.user.is_authenticated else "Anônimo",
        "profile": profile,
        "dias": dias,  # Passando os dias para o template
        "cores": cores,
        "periodos": periodos,
        "export_date": datetime.datetime.now(),
        'sidebar': 'agenda',
    }
    
    return render(request, "agenda.html", contexto)




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

    vinculos = VinculoProfissionalAtividade.objects.all().order_by("id_profissional")

    return render(request, "vinculos.html", {
        'vinculos': vinculos,
        'profile': profile,
        'sidebar': 'atividades'
    })

@login_required
def delete_vinculo(request, id_profissional, id_atividade):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    turma = get_object_or_404(Turma, pk=id_turma)

    if request.method == "POST":
        turma.delete()
        return redirect('turmas')

    return render(request, "turma_delete.html", {
        "turma": turma,
        "profile": profile,
        'sidebar': 'turmas'
    })


@login_required
def edit_vinculo(request, id_profissional, id_atividade):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    vinculo = get_object_or_404(VinculoProfissionalAtividade, id_profissional=id_profissional, id_atividade=id_atividade)

    if request.method == "POST":
        form = VinculoProfissionalAtividadeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('editar_profissional_atividade') 
    else:
        form = VinculoProfissionalAtividadeForm()

    return render(request, "create_vinculo.html", {
        "form": form,
        "vinculo": vinculo,
        "profile": profile,
        'sidebar': 'vinculos'
    })


@login_required
def new_vinculo(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == "POST":
        form = VinculoProfissionalAtividadeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vinculos') 
        else:
            messages.error(request, 'Essa relação entre o profissional e a atividade já existe.')
    else:
        form = VinculoProfissionalAtividadeForm()
        

    return render(request, "vinculo_create.html", {
        "form": form,
        "profile": profile,
        'sidebar': 'vínculos'
    })

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
def delete_turma(request, id_turma):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    turma = get_object_or_404(Turma, pk=id_turma)

    if request.method == "POST":
        turma.delete()
        return redirect('turmas')

    return render(request, "turma_delete.html", {
        "turma": turma,
        "profile": profile,
        'sidebar': 'turmas'
    })


@login_required
def edit_turma(request, id_turma):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    turma = get_object_or_404(Turma, pk=id_turma)

    if request.method == "POST":
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            return redirect('turmas')
    else:
        form = TurmaForm(instance=turma)

    return render(request, "turma_create.html", {
        "form": form,
        "turma": turma,
        "profile": profile,
        'sidebar': 'turmas'
    })


@login_required
def new_turma(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == "POST":
        form = TurmaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('turmas')
    else:
        form = TurmaForm()

    return render(request, "turma_create.html", {
        "form": form,
        "profile": profile,
        'sidebar': 'turmas'
    })

@login_required
def delete_atividade(request, id_atividade):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    atividade = get_object_or_404(Atividade, pk=id_atividade)

    if request.method == "POST":
        atividade.delete()
        return redirect('atividades')

    return render(request, "atividade_delete.html", {
        "atividade": atividade,
        "profile": profile,
        'sidebar': 'atividades'
    })


@login_required
def edit_atividade(request, id_atividade):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    atividade = get_object_or_404(Atividade, pk=id_atividade)

    if request.method == "POST":
        form = AtividadeForm(request.POST, instance=atividade)
        if form.is_valid():
            form.save()
            return redirect('atividades')
    else:
        form = AtividadeForm(instance=atividade)

    return render(request, "atividade_create.html", {
        "form": form,
        "atividade": atividade,
        "profile": profile,
        'sidebar': 'atividades'
    })


@login_required
def new_atividade(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == "POST":
        form = AtividadeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('atividades')
    else:
        form = AtividadeForm()

    return render(request, "atividade_create.html", {
        "form": form,
        "profile": profile,
        'sidebar': 'atividades'
    })


@login_required
def delete_profissional(request, id_profissional):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None 

    profissional = get_object_or_404(Profissional, id_profissional=id_profissional)

    if request.method == "POST":
        profissional.delete()
        return redirect('profissionais')
    
    return render(request, "profissional_delete.html", { "profissional": profissional, "profile": profile, 'sidebar': 'profissionais' })

@login_required
def edit_profissional(request, id_profissional):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None 

    profissional = get_object_or_404(Profissional, pk=id_profissional)

    if request.method == "POST":
        form = ProfissionalForm(request.POST, instance=profissional)
        if form.is_valid():
            form.save()
            return redirect('profissionais')
    else:
        form = ProfissionalForm(instance=profissional)

    return render(request, "profissional_create.html", { 
        "form": form, 
        "profissional": profissional, 
        "profile": profile, 
        'sidebar': 'profissionais' 
    })

def new_profissional(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None 

    if request.method == "POST":
        form = ProfissionalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profissionais')
    else:
        form = ProfissionalForm()

    return render(request, "profissional_create.html", { 
        "form": form, 
        "profile": profile, 
        'sidebar': 'profissionais' 
    })


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


@login_required
def editar_vinculo(request, id_atividade):
    atividade = get_object_or_404(Atividade, pk=id_atividade)

    if request.method == "POST":
        form = VinculoForm(request.POST, instance=atividade)
        if form.is_valid():
            form.save()
            messages.success(request, "Vínculo salvo com sucesso!")
            return redirect("atividades")  # Recarregar página após salvar
    else:
        form = VinculoForm(instance=atividade)

    return render(request, "editar_vinculo.html", {"form": form, "atividade": atividade})


@login_required
def script(request):
    atividades = Atividade.objects.all()
    response_data = []

    for atividade in atividades:
        turma = atividade.id_turma.first()
        profissional = atividade.id_profissional.first()

        response_data.append({
            "turma": turma.id_turma if turma else None,
            "prof": profissional.id_profissional if profissional else None,
            "ch": atividade.periodos,
            "duplas": 1 if atividade.id_caracteristica.nome == "Geminar" else 0,
            # "recurso": atividade.id_atividade.id_caracteristica.id_caracteristica if atividade.id_atividade.id_caracteristica else None
            "recurso": None,
        })

    print(response_data)

    def run_script_thread():
        resultado = run(response_data)

        salvar_matriz(resultado)

        
    thread = threading.Thread(target=run_script_thread)
    thread.start()
    return redirect("scriptst")


def scriptst(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None 

    f = open("oi.txt", "r+")
    valor = f.read()

    context = {"profile": profile, "status": valor}

    print(valor)

    if (valor == "2"):
        f.seek(0)
        f.write("0")
        f.truncate()

    return render(request, "status.html", context)


def atividades_view(request):
    atividades = Atividade.objects.all()
    response_data = []

    for atividade in atividades:
        turma = atividade.id_turma.first()
        profissional = atividade.id_profissional.first()

        response_data.append({
            "turma": turma.id_turma if turma else None,
            "prof": profissional.id_profissional if profissional else None,
            "ch": atividade.periodos,
            "duplas": 1 if atividade.id_caracteristica.nome == "Geminar" else 0,
            # "recurso": atividade.id_atividade.id_caracteristica.id_caracteristica if atividade.id_atividade.id_caracteristica else None
            "recurso": None,
        })

    return HttpResponse(response_data)