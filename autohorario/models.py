from django.db import models
from django.contrib.auth.models import User

class Caracteristica(models.Model):
    id_caracteristica = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.nome
    
class Profissional(models.Model):
    id_profissional = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, null=False)
    funcao = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    # imagem = models.ImageField(null=True, blank=True, upload_to="media/profile_pictures", default="Imagem_do_WhatsApp_de_2023-08-27_às_20.55.51.jpg")
    imagem = models.ImageField(null=True, blank=True, upload_to="oi")
    # id_atividade = models.ManyToManyField(Atividade, blank=True)

    # def publish(self):
    #     if self.imagem == None:
    #         self.imagem = 

    def __str__(self):
        return self.nome

class Turma(models.Model):
    id_turma = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, null=False)
    qnt_de_alunos = models.IntegerField()

    def __str__(self):
        return self.nome
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto_perfil = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Atividade(models.Model):
    id_atividade = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, null=False)
    carga_horaria = models.IntegerField()  # Carga Horária
    id_caracteristica = models.ForeignKey(Caracteristica, on_delete=models.PROTECT)
    # dia_da_semana = models.SmallIntegerField()  # Supondo 1 a 7 para os dias da semana
    periodos = models.SmallIntegerField()
    id_profissional = models.ManyToManyField(Profissional)
    id_turma = models.ManyToManyField(Turma)

    def __str__(self):
        return self.nome
class VinculoProfissionalAtividade(models.Model):
    id_atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    id_profissional = models.ManyToManyField(Profissional)
    id_turma = models.ManyToManyField(Turma)

    # class Meta:
    #     unique_together = ('id_profissional', 'id_atividade')
        
    def __str__(self):
        return f"{self.id_atividade.nome} - {self.id_profissional.nome}/{self.id_turma.nome}"