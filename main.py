import subprocess
import os
import config
import instagram
import time

def process_video(input_path):
    """
    Transforma el video al formato Reel y lo envía a subir.
    """
    if not os.path.exists(input_path):
        print(f"❌ Error: El video de entrada no existe en {input_path}")
        return False

    filename = os.path.basename(input_path)
    output_path = os.path.join(config.TEMP_FOLDER, f"final_{filename}")

    print(f"🛠️  Procesando con FFmpeg: {filename}")

    # Comando optimizado para Termux (Ultrafast + 9:16)
    ffmpeg_cmd = [
        'ffmpeg', '-y', '-i', input_path,
        '-vf', "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '23',
        '-c:a', 'aac', '-b:a', '128k',
        '-t', str(config.MAX_DURATION),
        output_path
    ]

    try:
        # Ejecutar procesamiento
        subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print("✂️  Video optimizado correctamente.")

        # Intentar subir
        success = instagram.upload_reel(output_path)
        
        # --- LIMPIEZA TOTAL ---
        # Esperamos 2 segundos para liberar archivos y borramos de la RAM
        time.sleep(2)
        if os.path.exists(input_path): os.remove(input_path)
        if os.path.exists(output_path): os.remove(output_path)
        print("🧹 Temporales eliminados. Memoria limpia.")
        
        return success

    except subprocess.CalledProcessError as e:
        print(f"🚨 Error en FFmpeg: {e}")
        return False
    except Exception as e:
        print(f"🚨 Error inesperado en el sistema: {e}")
        return False

if __name__ == "__main__":
    print("💡 Sistema V2 listo. Esperando disparador de bot.py")
