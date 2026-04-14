"""
Servicios de autenticación.
Funciones simples para validación y gestión de usuarios.
"""


def validar_email(email: str) -> bool:
    """Valida si un email tiene @ y un dominio."""
    if "@" not in email:
        return False
    if "." not in email:
        return False
    return True


def validar_fuerza_password(password: str) -> bool:
    """Valida que la contraseña tenga al menos 8 caracteres, mayúscula, minúscula y número."""
    if len(password) < 8:
        return False
    
    tiene_mayuscula = False
    tiene_minuscula = False
    tiene_numero = False
    
    for letra in password:
        if letra.isupper():
            tiene_mayuscula = True
        if letra.islower():
            tiene_minuscula = True
        if letra.isdigit():
            tiene_numero = True
    
    return tiene_mayuscula and tiene_minuscula and tiene_numero


def hashear_password(password: str) -> str:
    """Crea un hash simple de la contraseña."""
    hash_simple = ""
    for letra in password:
        hash_simple = hash_simple + str(ord(letra))
    return hash_simple


def crear_usuario(nombre: str, email: str, password: str):
    """Crea un usuario si los datos son válidos."""
    # Validar nombre
    if not nombre or len(nombre) < 2:
        return None
    
    # Validar email
    if not validar_email(email):
        return None
    
    # Validar password
    if not validar_fuerza_password(password):
        return None
    
    # Crear usuario
    usuario = {
        "nombre": nombre,
        "email": email,
        "password_hash": hashear_password(password)
    }
    
    return usuario

def validar_email(email: str) -> bool:
    """Valida si el formato del email es correcto."""
    return "@" in email and "." in email

def hashear_password(password: str) -> str:
    """Hashea una contraseña."""
    return f"hash_{password}"

