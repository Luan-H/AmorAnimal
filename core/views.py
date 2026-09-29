from django.shortcuts import render
from . import firebase_service

def home(request):
    animais = firebase_service.get_animais()
    patrocinadores = firebase_service.get_patrocinadores()
    
    context = {
        'animais': animais,
        'patrocinadores': patrocinadores,
    }
    return render(request, 'index.html', context)
