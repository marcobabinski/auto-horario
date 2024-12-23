from django.db import models
from django.contrib.auth.models import User

class Caracteristica(models.Model):
    id_caracteristica = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.nome

class Atividade(models.Model):
    id_atividade = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, null=False)
    carga_horaria = models.IntegerField()  # Carga Horária
    id_caracteristica = models.ForeignKey(Caracteristica, on_delete=models.PROTECT)
    dia_da_semana = models.SmallIntegerField()  # Supondo 1 a 7 para os dias da semana
    periodos = models.SmallIntegerField()

    def __str__(self):
        return self.nome
    
class Profissional(models.Model):
    id_profissional = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, null=False)
    funcao = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    id_atividade = models.ManyToManyField(Atividade)

    def __str__(self):
        return self.nome

class Turma(models.Model):
    id_turma = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, null=False)
    qnt_de_alunos = models.IntegerField()
    id_atividade = models.ManyToManyField(Atividade)

    def __str__(self):
        return self.nome
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto_perfil = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username