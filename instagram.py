from instagrapi import Client
import config
import os
import logging

def upload_reel(video_path, caption=config.DEFAULT_CAPTION):
    cl = Client()
    session_path = os.path.join(config.SESSIONS_FOLDER, f"{config.INSTA_USER}.json")
    
    try:
        # 1. Cargar sesión previa para evitar logueos constantes
        if os.path.exists(session_path):
            cl.load_settings(session_path)
            print(f"✅ Sesión de @{config.INSTA_USER} recuperada.")
        
        # 2. Login (usa las cookies si existen, si no, usa pass)
        cl.login(config.INSTA_USER, config.INSTA_PASS)
        cl.dump_settings(session_path) # Guardar cookies actualizadas
        
        print(f"🚀 Subiendo Reel a Instagram...")
        
        # 3. Subida con miniatura automática
        media = cl.clip_upload(
            video_path,
            caption=caption
        )
        
        print(f"✨ ¡ÉXITO! Reel publicado (ID: {media.pk})")
        return True

    except Exception as e:
        print(f"❌ Error en Instagram: {e}")
        return False
