import os
from pathlib import Path
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from django.conf import settings

_db = None

def get_firestore_client():
    global _db
    if _db is not None:
        return _db
        
    cred_path = getattr(settings, 'FIREBASE_CREDENTIALS_PATH', None)
    if not cred_path:
        cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH', 'firebase_credentials.json')
        
    full_path = Path(cred_path)
    if not full_path.is_absolute():
        full_path = settings.BASE_DIR / cred_path
        
    if not full_path.exists():
        # Procura qualquer arquivo de credenciais do firebase no diretório
        json_files = list(settings.BASE_DIR.glob('*firebase-adminsdk*.json'))
        if json_files:
            full_path = json_files[0]
            
    if full_path.exists():
        if not firebase_admin._apps:
            cred = credentials.Certificate(str(full_path))
            firebase_admin.initialize_app(cred)
        _db = firestore.client()
        return _db
    else:
        print(f"Aviso: Arquivo de credenciais do Firebase não encontrado em {full_path}")
        return None

# ==========================================
# CRUD: ANIMAIS
# ==========================================
def get_animais(status_filter=None):
    """Retorna lista de dicionários com todos os animais."""
    db = get_firestore_client()
    if not db:
        return []
    
    col = db.collection('animais')
    if status_filter:
        query = col.where('status_adocao', '==', status_filter)
    else:
        query = col
        
    docs = query.stream()
    animais = []
    for doc in docs:
        data = doc.to_dict()
        data['id'] = doc.id
        animais.append(data)
    return animais

def get_animal_by_id(animal_id):
    """Busca um animal específico pelo ID."""
    db = get_firestore_client()
    if not db or not animal_id:
        return None
    doc = db.collection('animais').document(animal_id).get()
    if doc.exists:
        data = doc.to_dict()
        data['id'] = doc.id
        return data
    return None

def create_animal(nome, historia, foto_antes_url, foto_depois_url, status_adocao='Disponível'):
    """Cria um novo animal no Firestore."""
    db = get_firestore_client()
    if not db:
        return None
    doc_ref = db.collection('animais').document()
    payload = {
        'nome': nome,
        'historia': historia,
        'foto_antes_url': foto_antes_url,
        'foto_depois_url': foto_depois_url,
        'status_adocao': status_adocao,
        'criado_em': datetime.now().isoformat(),
    }
    doc_ref.set(payload)
    payload['id'] = doc_ref.id
    return payload

def update_animal(animal_id, data):
    """Atualiza os dados de um animal existente."""
    db = get_firestore_client()
    if not db:
        return False
    data['atualizado_em'] = datetime.now().isoformat()
    db.collection('animais').document(animal_id).update(data)
    return True

def delete_animal(animal_id):
    """Exclui um animal do Firestore."""
    db = get_firestore_client()
    if not db:
        return False
    db.collection('animais').document(animal_id).delete()
    return True

# ==========================================
# CRUD: PATROCINADORES
# ==========================================
def get_patrocinadores(apenas_ativos=True):
    """Retorna lista de patrocinadores."""
    db = get_firestore_client()
    if not db:
        return []
    
    col = db.collection('patrocinadores')
    if apenas_ativos:
        query = col.where('ativo', '==', True)
    else:
        query = col
        
    docs = query.stream()
    patrocinadores = []
    for doc in docs:
        data = doc.to_dict()
        data['id'] = doc.id
        patrocinadores.append(data)
    return patrocinadores

def create_patrocinador(nome, link_externo, logotipo_url, ativo=True):
    """Cria um novo patrocinador no Firestore."""
    db = get_firestore_client()
    if not db:
        return None
    doc_ref = db.collection('patrocinadores').document()
    payload = {
        'nome': nome,
        'link_externo': link_externo,
        'logotipo_url': logotipo_url,
        'ativo': ativo,
        'criado_em': datetime.now().isoformat(),
    }
    doc_ref.set(payload)
    payload['id'] = doc_ref.id
    return payload

def delete_patrocinador(patrocinador_id):
    """Exclui um patrocinador."""
    db = get_firestore_client()
    if not db:
        return False
    db.collection('patrocinadores').document(patrocinador_id).delete()
    return True

# ==========================================
# REGISTRO DE PEDIDOS DE ADOÇÃO
# ==========================================
def create_adocao(animal_id, animal_nome, nome_interessado, telefone, mensagem=""):
    """Registra uma manifestação de interesse em adoção."""
    db = get_firestore_client()
    if not db:
        return None
    doc_ref = db.collection('adocoes').document()
    payload = {
        'animal_id': animal_id,
        'animal_nome': animal_nome,
        'nome_interessado': nome_interessado,
        'telefone': telefone,
        'mensagem': mensagem,
        'data_solicitacao': datetime.now().isoformat(),
        'status': 'Não visto' # 'Não visto', 'Em contato', 'Adotado'
    }
    doc_ref.set(payload)
    payload['id'] = doc_ref.id
    return payload

def get_adocoes():
    """Retorna todas as manifestações de interesse em adoção."""
    db = get_firestore_client()
    if not db:
        return []
    docs = db.collection('adocoes').order_by('data_solicitacao', direction=firestore.Query.DESCENDING).stream()
    adocoes = []
    for doc in docs:
        data = doc.to_dict()
        data['id'] = doc.id
        status = data.get('status')
        if not status or status == 'Pendente':
            data['status'] = 'Não visto'
        elif status == 'Contatado':
            data['status'] = 'Em contato'
        elif status == 'Concluído':
            data['status'] = 'Adotado'
        adocoes.append(data)
    return adocoes

def update_adocao_status(adocao_id, novo_status):
    """Atualiza o status de um pedido de adoção ('Não visto', 'Em contato', 'Adotado')."""
    db = get_firestore_client()
    if not db:
        return False
    doc_ref = db.collection('adocoes').document(adocao_id)
    doc_ref.update({'status': novo_status})
    return True

def delete_adocao(adocao_id):
    """Exclui um pedido de adoção."""
    db = get_firestore_client()
    if not db:
        return False
    db.collection('adocoes').document(adocao_id).delete()
    return True

# ==========================================
# CONFIGURAÇÕES E TEXTOS INSTITUCIONAIS
# ==========================================
CONFIG_PADRAO = {
    'hero_titulo': 'Amor Animal',
    'hero_subtitulo': 'Resgatando e transformando a vida de animais em Cuiabá.',
    'sobre_titulo': 'Sobre a ONG',
    'sobre_texto_1': (
        'Há aproximadamente 5 anos atrás , alguns protetores independentes se reuniram '
        'com o propósito de formar uma organização não governamental (ONG) que tornasse '
        'possível assistir, com um pouco mais de dignidade, cães em estado de abandono e vulnerabilidade.'
    ),
    'sobre_texto_2': (
        'A Associação Amor Animal atua como entidade que oferta serviços de forma continuada, '
        'permanente e planejada, direcionados à prevenção e mitigação da vulnerabilidade de animais '
        'abandonados, captando doações de pessoas físicas e/ou jurídicas, dos setores privados e/ou '
        'públicos e atua também de forma proativa com informações e conhecimento sobre as causas e '
        'impactos negativos do abandono de animais na sociedade.'
    ),
    'chave_pix': '49.671.733/0001-47',
    'instagram_usuario': '@amoranimal.cuiaba',
    'instagram_link': 'https://www.instagram.com/amoranimal.cuiaba',
    'whatsapp_numero': '(65) 9 8119-3351',
    'whatsapp_link': 'https://wa.me/5565981193351?text=Ol%C3%A1%2C%20vim%20do%20site%21',
}

def get_configuracoes():
    """Retorna as configurações e textos institucionais da ONG."""
    db = get_firestore_client()
    if not db:
        return CONFIG_PADRAO.copy()
    
    doc = db.collection('configuracoes').document('institucional').get()
    if doc.exists:
        dados = doc.to_dict()
        cfg = CONFIG_PADRAO.copy()
        cfg.update(dados)
        return cfg
    return CONFIG_PADRAO.copy()

def save_configuracoes(dados):
    """Salva configurações e textos da ONG no Firestore."""
    db = get_firestore_client()
    if not db:
        return False
    dados['atualizado_em'] = datetime.now().isoformat()
    db.collection('configuracoes').document('institucional').set(dados, merge=True)
    return True

def seed_initial_data_if_empty():
    """Popula os 3 cães e 4 patrocinadores originais no Firestore se ainda estiver vazio."""
    db = get_firestore_client()
    if not db:
        return False
    
    # 1. Animais
    animais_existentes = list(db.collection('animais').limit(1).stream())
    if not animais_existentes:
        animais_base = [
            {
                'nome': 'Negão',
                'historia': 'Resgatado em situação de rua extrema, recebeu todos os tratamentos veterinários e hoje está totalmente recuperado e saudável.',
                'foto_antes_url': '/static/img/ne-antes.jpeg',
                'foto_depois_url': '/static/img/ne-depois.jpeg',
                'status_adocao': 'Disponível',
                'criado_em': datetime.now().isoformat(),
            },
            {
                'nome': 'Vitória',
                'historia': 'Sobreviveu a graves maus-tratos, passou por reabilitação completa e com muito carinho recuperou a alegria de viver.',
                'foto_antes_url': '/static/img/vi-antes.jpeg',
                'foto_depois_url': '/static/img/vi-depois.jpeg',
                'status_adocao': 'Disponível',
                'criado_em': datetime.now().isoformat(),
            },
            {
                'nome': 'Pretinha',
                'historia': 'Acolhida após abandono, foi tratada contra desnutrição e hoje é dócil, brincalhona e pronta para uma família amorosa.',
                'foto_antes_url': '/static/img/antes.jpeg',
                'foto_depois_url': '/static/img/depois.jpeg',
                'status_adocao': 'Disponível',
                'criado_em': datetime.now().isoformat(),
            },
        ]
        for a in animais_base:
            db.collection('animais').document().set(a)

    # 2. Patrocinadores
    patrocinadores_existentes = list(db.collection('patrocinadores').limit(1).stream())
    if not patrocinadores_existentes:
        patrocinadores_base = [
            {
                'nome': 'MedPort',
                'link_externo': 'https://www.instagram.com/clinicamedport/',
                'logotipo_url': '/static/img/medport_img.jpg',
                'ativo': True,
                'criado_em': datetime.now().isoformat(),
            },
            {
                'nome': 'PetSee',
                'link_externo': 'https://www.instagram.com/petsee_pet/',
                'logotipo_url': '/static/img/petsee_img.jpg',
                'ativo': True,
                'criado_em': datetime.now().isoformat(),
            },
            {
                'nome': 'PetMarket',
                'link_externo': 'https://www.instagram.com/petmarketcuiaba/',
                'logotipo_url': '/static/img/petmarket_img.jpg',
                'ativo': True,
                'criado_em': datetime.now().isoformat(),
            },
            {
                'nome': 'Ministério Público de Mato Grosso',
                'link_externo': 'https://www.instagram.com/mpemt/',
                'logotipo_url': '/static/img/mpmt_img.jpg',
                'ativo': True,
                'criado_em': datetime.now().isoformat(),
            },
        ]
        for p in patrocinadores_base:
            db.collection('patrocinadores').document().set(p)

    # 3. Configurações
    cfg_doc = db.collection('configuracoes').document('institucional').get()
    if not cfg_doc.exists:
        save_configuracoes(CONFIG_PADRAO)

    return True

