from django.shortcuts import render, redirect
from django.contrib import messages
from . import firebase_service
from .forms import SolicitacaoAdocaoForm

def home(request):
    if request.method == 'POST' and 'solicitar_adocao' in request.POST:
        form_adocao = SolicitacaoAdocaoForm(request.POST)
        if form_adocao.is_valid():
            animal_id = form_adocao.cleaned_data['animal_id']
            animal_nome = form_adocao.cleaned_data['animal_nome']
            nome_interessado = form_adocao.cleaned_data['nome_interessado']
            telefone = form_adocao.cleaned_data['telefone']
            mensagem = form_adocao.cleaned_data['mensagem']

            firebase_service.create_adocao(
                animal_id=animal_id,
                animal_nome=animal_nome,
                nome_interessado=nome_interessado,
                telefone=telefone,
                mensagem=mensagem
            )
            messages.success(request, f'Obrigado pelo seu interesse em adotar {animal_nome}! A equipe da ONG entrará em contato com você pelo WhatsApp.')
            return redirect('core:home')
        else:
            messages.error(request, 'Por favor, preencha corretamente os campos para solicitar a adoção.')

    animais = firebase_service.get_animais()
    patrocinadores = firebase_service.get_patrocinadores(apenas_ativos=True)
    config = firebase_service.get_configuracoes()
    
    context = {
        'animais': animais,
        'patrocinadores': patrocinadores,
        'config': config,
    }
    return render(request, 'index.html', context)

