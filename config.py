import os

# --- IDENTIDAD Y TOKENS ---
TELEGRAM_TOKEN = "TU_BOT_TOKEN_AQUÍ"
CHANNEL_ID = -1003584710096  # Reemplaza con el ID de tu canal

# --- INSTAGRAM AUTH ---
INSTA_USER = "tu_usuario"
INSTA_PASS = "tu_password"

# --- RUTAS DE SISTEMA (OPTIMIZADO PARA TERMUX) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Intentar usar RAM Disk para velocidad 10x, si falla usa disco
TEMP_FOLDER = "/dev/shm/mally_temp" 
if not os.path.exists("/dev/shm"):
    TEMP_FOLDER = os.path.join(BASE_DIR, "temp")

SESSIONS_FOLDER = os.path.join(BASE_DIR, "sessions")

# Crear carpetas necesarias
for folder in [TEMP_FOLDER, SESSIONS_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# --- CONFIGURACIÓN DE VIDEO ---
MAX_DURATION = 60  
DEFAULT_CAPTION = "🔥 Nuevo Reel Automático #MallySeries #ImperioMP"
