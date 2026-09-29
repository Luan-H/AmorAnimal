from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import firebase_service
from . import storage_service
from .forms import LoginForm, AnimalForm, PatrocinadorForm

# ==========================================
# AUTENTICAÇÃO
# ==========================================
def painel_login(request):
    if request.user.is_authenticated:
        return redirect('core:painel_dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo(a), {user.username}!')
                return redirect('core:painel_dashboard')
            else:
                messages.error(request, 'Usuário ou senha incorretos.')
    else:
        form = LoginForm()

    return render(request, 'painel/login.html', {'form': form})

def painel_logout(request):
    logout(request)
    messages.info(request, 'Você saiu do painel com segurança.')
    return redirect('core:painel_login')

# ==========================================
# DASHBOARD
# ==========================================
@login_required(login_url='core:painel_login')
def painel_dashboard(request):
    animais = firebase_service.get_animais()
    patrocinadores = firebase_service.get_patrocinadores(apenas_ativos=False)
    adocoes = firebase_service.get_adocoes()

    total_animais = len(animais)
    adotados = sum(1 for a in animais if a.get('status_adocao') == 'Adotado')
    disponiveis = sum(1 for a in animais if a.get('status_adocao') == 'Disponível')
    total_patrocinadores = len(patrocinadores)
    total_adocoes = len(adocoes)

    context = {
        'total_animais': total_animais,
        'adotados': adotados,
        'disponiveis': disponiveis,
        'total_patrocinadores': total_patrocinadores,
        'total_adocoes': total_adocoes,
        'ultimos_animais': animais[:4],
        'ultimas_adocoes': adocoes[:5],
    }
    return render(request, 'painel/dashboard.html', context)

# ==========================================
# GESTÃO DE ANIMAIS
# ==========================================
@login_required(login_url='core:painel_login')
def animal_list(request):
    animais = firebase_service.get_animais()
    return render(request, 'painel/animal_list.html', {'animais': animais})

@login_required(login_url='core:painel_login')
def animal_create(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            historia = form.cleaned_data['historia']
            status_adocao = form.cleaned_data['status_adocao']

            foto_antes_url = ''
            foto_depois_url = ''

            if 'foto_antes' in request.FILES:
                foto_antes_url = storage_service.upload_image(request.FILES['foto_antes'], folder='animais')
            if 'foto_depois' in request.FILES:
                foto_depois_url = storage_service.upload_image(request.FILES['foto_depois'], folder='animais')

            firebase_service.create_animal(
                nome=nome,
                historia=historia,
                foto_antes_url=foto_antes_url,
                foto_depois_url=foto_depois_url,
                status_adocao=status_adocao
            )
            messages.success(request, f'O cãozinho "{nome}" foi cadastrado com sucesso!')
            return redirect('core:animal_list')
    else:
        form = AnimalForm()

    return render(request, 'painel/animal_form.html', {'form': form, 'titulo': 'Cadastrar Novo Animal'})

@login_required(login_url='core:painel_login')
def animal_edit(request, animal_id):
    animal = firebase_service.get_animal_by_id(animal_id)
    if not animal:
        messages.error(request, 'Animal não encontrado.')
        return redirect('core:animal_list')

    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            data_to_update = {
                'nome': form.cleaned_data['nome'],
                'historia': form.cleaned_data['historia'],
                'status_adocao': form.cleaned_data['status_adocao'],
            }

            if 'foto_antes' in request.FILES:
                data_to_update['foto_antes_url'] = storage_service.upload_image(request.FILES['foto_antes'], folder='animais')
            if 'foto_depois' in request.FILES:
                data_to_update['foto_depois_url'] = storage_service.upload_image(request.FILES['foto_depois'], folder='animais')

            firebase_service.update_animal(animal_id, data_to_update)
            messages.success(request, f'Dados de "{form.cleaned_data["nome"]}" atualizados com sucesso!')
            return redirect('core:animal_list')
    else:
        initial_data = {
            'nome': animal.get('nome', ''),
            'historia': animal.get('historia', ''),
            'status_adocao': animal.get('status_adocao', 'Disponível'),
        }
        form = AnimalForm(initial=initial_data)

    context = {
        'form': form,
        'animal': animal,
        'titulo': f'Editar {animal.get("nome")}',
    }
    return render(request, 'painel/animal_form.html', context)

@login_required(login_url='core:painel_login')
def animal_delete(request, animal_id):
    if request.method == 'POST':
        animal = firebase_service.get_animal_by_id(animal_id)
        nome = animal.get('nome') if animal else 'Animal'
        firebase_service.delete_animal(animal_id)
        messages.success(request, f'"{nome}" foi removido do sistema.')
    return redirect('core:animal_list')

# ==========================================
# GESTÃO DE PATROCINADORES
# ==========================================
@login_required(login_url='core:painel_login')
def patrocinador_list(request):
    patrocinadores = firebase_service.get_patrocinadores(apenas_ativos=False)
    return render(request, 'painel/patrocinador_list.html', {'patrocinadores': patrocinadores})

@login_required(login_url='core:painel_login')
def patrocinador_create(request):
    if request.method == 'POST':
        form = PatrocinadorForm(request.POST, request.FILES)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            link_externo = form.cleaned_data['link_externo']
            ativo = form.cleaned_data['ativo']

            logotipo_url = ''
            if 'logotipo' in request.FILES:
                logotipo_url = storage_service.upload_image(request.FILES['logotipo'], folder='patrocinadores')

            firebase_service.create_patrocinador(
                nome=nome,
                link_externo=link_externo,
                logotipo_url=logotipo_url,
                ativo=ativo
            )
            messages.success(request, f'Patrocinador "{nome}" adicionado com sucesso!')
            return redirect('core:patrocinador_list')
    else:
        form = PatrocinadorForm()

    return render(request, 'painel/patrocinador_form.html', {'form': form, 'titulo': 'Adicionar Patrocinador'})

@login_required(login_url='core:painel_login')
def patrocinador_delete(request, patrocinador_id):
    if request.method == 'POST':
        firebase_service.delete_patrocinador(patrocinador_id)
        messages.success(request, 'Patrocinador removido com sucesso.')
    return redirect('core:patrocinador_list')

# ==========================================
# GESTÃO DE ADOÇÕES
# ==========================================
@login_required(login_url='core:painel_login')
def adocao_list(request):
    adocoes = firebase_service.get_adocoes()
    return render(request, 'painel/adocao_list.html', {'adocoes': adocoes})
