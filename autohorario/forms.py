import datetime
from django.contrib.auth.backends import UserModel
from django.db.models import fields
from django import forms
from .models import Turma
from .models import Profissional
from .models import Atividade
from .models import Caracteristica

class FormLogin(forms.Form):
    usuario = forms.CharField(label='Usuário', max_length=20)
    senha = forms.CharField(widget=forms.PasswordInput, min_length=5, max_length=20)

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'qnt_de_alunos']  # Substitua pelos campos reais do modelo.
    
        labels = {
                'qnt_de_alunos': ('Quantidade de Alunos'),
            }

class ProfissionalForm(forms.ModelForm):
    # id_atividade = forms.ModelMultipleChoiceField(
    #     queryset=Atividade.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     label="Atividades"
    # )
    
    class Meta:
        model = Profissional
        fields = ['nome', 'funcao', 'endereco', 'imagem',]
        labels = {
            'nome': 'Nome do Profissional',
            'endereco': 'Endereço',
            'funcao': 'Função',
        }

class AtividadeForm(forms.ModelForm):
    id_caracteristica = forms.ModelChoiceField(
        queryset=Caracteristica.objects.all(),
        label="Categoria",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Selecione uma categoria" 
    )

    dia_da_semana = forms.ChoiceField(
        choices=[(1, 'Domingo'), (2, 'Segunda-feira'), (3, 'Terça-feira'), 
                 (4, 'Quarta-feira'), (5, 'Quinta-feira'), (6, 'Sexta-feira'), 
                 (7, 'Sábado')],
        label="Dia da Semana",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    periodos = forms.IntegerField(
        min_value=1,
        max_value=10,  # Ajuste conforme suas regras
        label="Períodos",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Atividade
        fields = ['nome', 'carga_horaria', 'id_caracteristica', 'dia_da_semana', 'periodos']
        labels = {
            'nome': 'Nome da Atividade',
            'carga_horaria': 'Carga Horária',
        }