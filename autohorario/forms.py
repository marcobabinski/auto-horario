import datetime
from django.contrib.auth.backends import UserModel
from django.db.models import fields
from django import forms
from .models import Turma
from .models import Profissional
from .models import Atividade
from .models import Caracteristica
from .models import VinculoProfissionalAtividade
from django.core.exceptions import ValidationError

class FormLogin(forms.Form):
    usuario = forms.CharField(label='Usuário', max_length=20)
    senha = forms.CharField(widget=forms.PasswordInput, min_length=5, max_length=20)

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'qnt_de_alunos'] 
    
        labels = {
                'qnt_de_alunos': ('Quantidade de Alunos'),
            }
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-green-500 focus:border-green-500'
            }),
            'qnt_de_alunos': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-green-500 focus:border-green-500'
            }),
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
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-green-500 focus:border-green-500'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-green-500 focus:border-green-500'
            }),
            'funcao': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-green-500 focus:border-green-500'
            }),
        }

class AtividadeForm(forms.ModelForm):
    id_caracteristica = forms.ModelChoiceField(
        queryset=Caracteristica.objects.all(),
        label="Categoria",
        widget=forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-green-500 focus:border-green-500'
        }),
        empty_label="Selecione uma categoria" 
    )

    dia_da_semana = forms.ChoiceField(
        choices=[(1, 'Domingo'), (2, 'Segunda-feira'), (3, 'Terça-feira'), 
                 (4, 'Quarta-feira'), (5, 'Quinta-feira'), (6, 'Sexta-feira'), 
                 (7, 'Sábado')],
        label="Dia da Semana",
        widget=forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-green-500 focus:border-green-500'
        }),
    )
    
    periodos = forms.IntegerField(
        min_value=1,
        max_value=10,  # Ajuste conforme suas regras
        label="Períodos",
        widget=forms.NumberInput(attrs={
            'class': 'w-full border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-green-500 focus:border-green-500'
        })
    )

    class Meta:
        model = Atividade
        fields = ['nome', 'carga_horaria', 'id_caracteristica', 'dia_da_semana', 'periodos']
        labels = {
            'nome': 'Nome da Atividade',
            'carga_horaria': 'Carga Horária',
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-green-500 focus:border-green-500'
            }),
            'carga_horaria': forms.NumberInput(attrs={
                'class': 'w-full border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-green-500 focus:border-green-500'
            }),
        }

class VinculoProfissionalAtividadeForm(forms.ModelForm):
    id_profissional = forms.ModelChoiceField(
        queryset=Profissional.objects.all(),
        label="Profissional",
        widget=forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-green-500 focus:border-green-500'
        }),
        empty_label="Selecione um profissional" 
    )

    id_atividade = forms.ModelChoiceField(
        queryset=Atividade.objects.all(),
        label="Atividade",
        widget=forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-green-500 focus:border-green-500'
        }),
        empty_label="Selecione uma atividades" 
    )

    class Meta:
        model = VinculoProfissionalAtividade
        fields = ['id_profissional', 'id_atividade']

    def clean(self):
        cleaned_data = super().clean()
        id_profissional = cleaned_data.get('id_profissional')
        id_atividade = cleaned_data.get('id_atividade')

        if VinculoProfissionalAtividade.objects.filter(id_profissional=id_profissional, id_atividade=id_atividade).exists():
            raise ValidationError(
                {"id_profissional": "Essa relação entre o profissional e a atividade já existe."}
            )

        return cleaned_data