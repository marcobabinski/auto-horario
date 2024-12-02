import datetime
from django.contrib.auth.backends import UserModel
from django.db.models import fields
from django import forms
from .models import Turma

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