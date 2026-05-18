"""
Configuración de la aplicación FastAPI.
Variables de entorno y constantes globales.
"""

import os
from datetime import timedelta

# ==================== APLICACIÓN ====================
APP_NAME = "Sistema de Gestión de Incidencias de Tráfico"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "API para reportar y gestionar incidencias de tráfico"
DEBUG = os.getenv("DEBUG", "False") == "True"

# ==================== SERVIDOR ====================
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
RELOAD = os.getenv("RELOAD", "True") == "True"

# ==================== SEGURIDAD ====================
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "tu-clave-secreta-muy-segura-cambiar-en-produccion-123456"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ACCESS_TOKEN_EXPIRE_DELTA = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

# ==================== VALIDACIONES ====================
# Usuarios
MIN_NOMBRE_LENGTH = 2
MAX_NOMBRE_LENGTH = 100
MAX_EMAIL_LENGTH = 255

# Contraseñas
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128

# Reportes
MIN_TITULO_LENGTH = 3
MAX_TITULO_LENGTH = 200
MIN_UBICACION_LENGTH = 3
MAX_UBICACION_LENGTH = 200
MAX_DESCRIPCION_LENGTH = 500

# Tipos de incidencias válidos
TIPOS_INCIDENCIA = [
    "semaforo",
    "bache",
    "poste",
    "alcantarilla",
    "señalizacion",
    "otro"
]

# Estados válidos
ESTADOS_INCIDENCIA = [
    "abierto",
    "en_progreso",
    "cerrado"
]

# Prioridades válidas
PRIORIDADES_INCIDENCIA = [
    "baja",
    "media",
    "alta"
]

# ==================== ARCHIVOS ====================
UPLOAD_DIR = "static/uploads"
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

# ==================== BASE DE DATOS ====================
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/incidencias.db")
SQLALCHEMY_ECHO = DEBUG
SQLALCHEMY_POOL_PRE_PING = True

# ==================== LOGGING ====================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ==================== CORS ====================
ALLOW_ORIGINS = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
]

# ==================== MENSAJES ====================

MENSAJES = {
    "registro_exitoso": "Usuario registrado exitosamente",
    "login_exitoso": "Sesión iniciada correctamente",
    "reporte_creado": "Reporte creado exitosamente",
    "foto_subida": "Foto subida exitosamente",
    "email_duplicado": "El email ya está registrado",
    "credenciales_invalidas": "Email o contraseña incorrectos",
    "token_invalido": "Token inválido o expirado",
    "no_autenticado": "Usuario no autenticado",
    "campo_requerido": "Este campo es requerido",
    "formato_invalido": "Formato inválido",
    "error_servidor": "Error interno del servidor",
}


if __name__ == "__main__":
    # Mostrar configuración en consola
    print(f"🚗 {APP_NAME} v{APP_VERSION}")
    print(f"🔑 SECRET_KEY configurada: {'Sí' if SECRET_KEY != 'tu-clave-secreta-muy-segura-cambiar-en-produccion-123456' else '⚠️ NO - Usar valor por defecto'}")
    print(f"📊 Base de datos: {DATABASE_URL}")
    print(f"🌐 Servidor: {HOST}:{PORT}")
