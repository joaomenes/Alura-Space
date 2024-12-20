from django.shortcuts import render, get_object_or_404
from galeria.models import Fotografia
import unicodedata

def remover_acentos(texto):
    #Remove os acentos de uma string.
    return ''.join(
        char for char in unicodedata.normalize('NFD', texto)
        if unicodedata.category(char) != 'Mn'
    )

def index(request):
    fotografias = Fotografia.objects.order_by("data_fotografia").filter(publicado=True)
    return render(request, 'galeria/index.html', {"cards": fotografias})

def imagem(request, foto_id):
    fotografia = get_object_or_404(Fotografia, pk=foto_id)
    return render(request, 'galeria/imagem.html', {"fotografia": fotografia})

def buscar(request):
    fotografias = Fotografia.objects.order_by("data_fotografia").filter(publicado=True)

    if "buscar" in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            nome_a_buscar_sem_acento = remover_acentos(nome_a_buscar).lower()
            #trazer os dados do banco
            fotografias = [
                foto for foto in fotografias
                if remover_acentos(foto.nome.lower()).find(nome_a_buscar_sem_acento) != -1
            ]

    return render(request, "galeria/buscar.html", {"cards": fotografias})
