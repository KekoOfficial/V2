from instagrapi import Client
import config
import os

def upload_reel(video_path, caption=config.DEFAULT_CAPTION):
    cl = Client()
    session_path = os.path.join(config.SESSIONS_FOLDER, f"{config.INSTA_USER}.json")
    
    try:
        # Intentar cargar sesión guardada
        if os.path.exists(session_path):
            cl.load_settings(session_path)
            print(f"✅ Sesión de {config.INSTA_USER} cargada.")
        
        cl.login(config.INSTA_USER, config.INSTA_PASS)
        cl.dump_settings(session_path) # Guardar/Actualizar cookies
        
        print(f"🚀 Subiendo Reel a @{config.INSTA_USER}...")
        
        # Subida oficial
        media = cl.clip_upload(
            video_path,
            caption=caption
        )
        
        print(f"✨ Éxito: Reel publicado (ID: {media.pk})")
        return True

    except Exception as e:
        print(f"❌ Error crítico en Instagram: {e}")
        return False
