from django.http import HttpResponse

def index(request):
    nome = "Gustavo Lima"
    return HttpResponse(f"Olár {nome}")