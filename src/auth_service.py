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




