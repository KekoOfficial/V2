import subprocess
import os
import config
import instagram
import time
import logging

# Configuración de logs para ver qué pasa en la consola
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_video(input_path):
    """
    Orquestador: Procesa el video de Telegram y lo sube a Instagram.
    """
    if not os.path.exists(input_path):
        logging.error(f"❌ El archivo de entrada no existe: {input_path}")
        return False

    # Definir ruta de salida en la RAM (más rápido) o Carpeta temporal
    filename = os.path.basename(input_path)
    output_path = os.path.join(config.TEMP_FOLDER, f"reel_{filename}")

    logging.info(f"🛠️  Iniciando optimización de video: {filename}")

    # COMANDO FFmpeg IMPERIAL:
    # 1. -y: Sobrescribir si existe.
    # 2. -vf: Escala a 1080:1920, recorta para 9:16 perfecto.
    # 3. -c:v libx264: El códec más compatible.
    # 4. -preset ultrafast: Máxima velocidad en Termux.
    # 5. -t 59: Asegura que no pase de 1 min (límite Reel estándar).
    ffmpeg_cmd = [
        'ffmpeg', '-y', '-i', input_path,
        '-vf', "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '23',
        '-c:a', 'aac', '-b:a', '128k',
        '-t', '59',
        output_path
    ]

    try:
        # Ejecutar FFmpeg
        logging.info("✂️  Cortando y renderizando...")
        subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
        if os.path.exists(output_path):
            logging.info("✅ Procesamiento terminado. Iniciando subida a Instagram...")
            
            # Intentar la subida con el módulo instagram.py
            success = instagram.upload_reel(output_path)
            
            if success:
                logging.info("🚀 REEL PUBLICADO CON ÉXITO EN EL IMPERIO")
            else:
                logging.error("❌ La subida falló. Revisa las credenciales o conexión.")

            # --- LIMPIEZA DE HUELLAS ---
            # Esperamos un segundo para liberar el archivo y borrar
            time.sleep(2)
            try:
                if os.path.exists(input_path): os.remove(input_path)
                if os.path.exists(output_path): os.remove(output_path)
                logging.info("🧹 Limpieza de temporales completada.")
            except Exception as e:
                logging.warning(f"⚠️ No se pudo borrar algún temporal: {e}")
            
            return success
        else:
            logging.error("⚠️ FFmpeg no generó el archivo de salida.")
            return False

    except subprocess.CalledProcessError as e:
        logging.error(f"🚨 Error crítico en FFmpeg (¿Está instalado?): {e}")
        return False
    except Exception as e:
        logging.error(f"🚨 Error inesperado en main.py: {e}")
        return False

if __name__ == "__main__":
    # Prueba manual: puedes poner la ruta de un mp4 aquí para probar solo este archivo
    # process_video("test.mp4")
    print("💡 Sistema V2: Este módulo espera órdenes de bot.py")
