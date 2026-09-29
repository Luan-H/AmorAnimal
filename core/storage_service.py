import os
import uuid
from pathlib import Path
from django.conf import settings
import cloudinary
import cloudinary.uploader

def is_cloudinary_configured():
    cfg = settings.CLOUDINARY_STORAGE
    return bool(cfg.get('CLOUD_NAME') and cfg.get('API_KEY') and cfg.get('API_SECRET'))

def upload_image(file_obj, folder='animais'):
    """
    Faz upload de imagem para o Cloudinary se configurado.
    Caso contrário, salva localmente na pasta media/ como fallback de desenvolvimento.
    Retorna a URL pública acessível da imagem.
    """
    if is_cloudinary_configured():
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
            api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
            api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'],
            secure=True
        )
        response = cloudinary.uploader.upload(
            file_obj,
            folder=f"amor_animal/{folder}",
            resource_type="image"
        )
        return response.get('secure_url')
    
    # Fallback local (salva em media/<folder>/)
    ext = Path(file_obj.name).suffix or '.jpg'
    filename = f"{uuid.uuid4().hex}{ext}"
    dest_dir = settings.MEDIA_ROOT / folder
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / filename
    
    with open(dest_path, 'wb+') as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)
            
    return f"{settings.MEDIA_URL}{folder}/{filename}"
