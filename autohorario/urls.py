"""
URL configuration for autohorario project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.fazer_login, name="fazer_login"),
    path('logout/', views.fazer_logout, name='fazer_logout'),
    path('recuperar-senha/', views.recoverPassword, name="recover password"),
    # path('profissionais', views.profissionais, name="profissionais"),
    # path('agenda', views.agenda, name="agenda"),
    # path('turmas', views.turmas, name="turmas"),
    # path('vinculos', views.vinculos, name="vinculos"),
    # path('atividades', views.atividades, name="atividades"),
    # path('atividades/delete/<int:id_atividade>/', views.delete_atividade, name='delete_atividade'),
    # path('atividades/edit/<int:id_atividade>/', views.edit_atividade, name='edit_atividade'),
    # path('turmas/delete/<int:id_turma>/', views.delete_turma, name='delete_turma'),
    # path('turmas/edit/<int:id_turma>/', views.edit_turma, name='edit_turma'),
    # path('profissionais/delete/<int:id_profissional>/', views.delete_profissional, name='delete_profissional'),
    # path('profissionais/edit/<int:id_profissional>/', views.edit_profissional, name='edit_profissional'),
    path('teste/', views.teste, name="teste"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('dashboard/<str:screen>/', views.dashboard_load_screen, name="dashboard_load_screen"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)