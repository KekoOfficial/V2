import subprocess
import os
import config
import instagram

def process_video(input_path):
    # Generar nombre de salida en la carpeta temporal
    filename = os.path.basename(input_path)
    output_path = os.path.join(config.TEMP_FOLDER, f"processed_{filename}")

    print(f"🛠️ Optimizando video para Instagram...")

    # Comando FFmpeg PRO:
    # 1. Fuerza 1080x1920 (9:16)
    # 2. Usa libx264 para máxima compatibilidad
    # 3. Corta a 60 segundos si es más largo
    ffmpeg_cmd = [
        'ffmpeg', '-y', '-i', input_path,
        '-vf', "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '23',
        '-c:a', 'aac', '-b:a', '128k',
        '-t', str(config.MAX_DURATION),
        output_path
    ]

    try:
        # Ejecutar FFmpeg de forma silenciosa
        subprocess.run(ffmpeg_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print("✂️ Video procesado con éxito.")

        # Intentar la subida
        success = instagram.upload_reel(output_path)
        
        # LIMPIEZA TOTAL (Invisible)
        if os.path.exists(input_path): os.remove(input_path)
        if os.path.exists(output_path): os.remove(output_path)
        
        return success

    except Exception as e:
        print(f"❌ Error en el procesamiento: {e}")
        return False
