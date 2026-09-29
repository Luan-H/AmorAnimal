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
        'status': 'Pendente' # Pendente, Contatado, Concluído
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
        adocoes.append(data)
    return adocoes
