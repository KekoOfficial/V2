import telebot
import config
import main
import os
import logging

# Configurar el bot con tu Token de config.py
bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

print("📡 [IMPERIO V2] Escuchando el canal... (Presiona Ctrl+C para detener)")

@bot.channel_post_handler(content_types=['video'])
def handle_channel_video(message):
    # 1. Validar que el video venga del canal autorizado
    if message.chat.id == config.CHANNEL_ID:
        try:
            print(f"📥 Nuevo video detectado en: {message.chat.title}")
            
            # 2. Obtener info del archivo
            file_info = bot.get_file(message.video.file_id)
            
            # 3. Definir ruta de descarga en RAM (Velocidad Imperial)
            download_path = os.path.join(config.TEMP_FOLDER, f"raw_{message.video.file_id}.mp4")
            
            print("⏳ Descargando video desde Telegram...")
            downloaded_file = bot.download_file(file_info.file_path)
            
            with open(download_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            
            print("✅ Descarga exitosa. Enviando a procesar...")
            
            # 4. DISPARAR EL MAIN.PY
            # Aquí es donde ocurre la magia: recorta, optimiza y sube a Instagram
            main.process_video(download_path)
            
        except Exception as e:
            print(f"🚨 Error procesando el post del canal: {e}")
    else:
        # Esto ignora mensajes de otros canales donde el bot pueda estar
        print(f"⚠️ Mensaje ignorado de chat ID: {message.chat.id}")

# Lanzar el bot en modo infinito (resistente a micro-cortes de internet)
if __name__ == "__main__":
    try:
        bot.polling(non_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(f"🚨 El bot se detuvo: {e}")
