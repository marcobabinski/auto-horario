import datetime
from django.contrib.auth.backends import UserModel
from django.db.models import fields
from django import forms

class FormLogin(forms.Form):
    usuario = forms.CharField(label='Usuário', max_length=20)
    senha = forms.CharField(widget=forms.PasswordInput, min_length=5, max_length=20)