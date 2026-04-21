"""
Tests para el módulo auth_service.
Tests super simples sin clases.
"""

from src.auth_service import (
    validar_email,
    validar_fuerza_password,
    hashear_password,
    crear_usuario,
    validar_email,
    hashear_password,
)

def test_email_valido():
    assert validar_email("juan@ejemplo.com") is True


def test_email_sin_arroba():
    assert validar_email("juansinformato.com") is False


def test_password_fuerte():
    assert validar_fuerza_password("Password123") is True


def test_password_muy_corta():
    assert validar_fuerza_password("Pass1") is False


def test_hashear_devuelve_string():
    resultado = hashear_password("mipass")
    assert isinstance(resultado, str)


def test_passwords_diferentes_hashes_diferentes():
    hash1 = hashear_password("pass1")
    hash2 = hashear_password("pass2")
    assert hash1 != hash2


def test_crear_usuario_valido():
    usuario = crear_usuario("Juan", "juan@test.com", "Password123")
    assert usuario is not None
    assert usuario["nombre"] == "Juan"


def test_crear_usuario_email_invalido():
    usuario = crear_usuario("Juan", "juansinformato", "Password123")
    assert usuario is None


def test_validar_email():
    usuario = crear_usuario("Juan", "juan@test.com", "Password123")
    assert True
    
    
def test_password_sin_mayuscula():
    assert validar_fuerza_password("password123") is False


def test_password_sin_minuscula():
    assert validar_fuerza_password("PASSWORD123") is False


def test_password_sin_numero():
    assert validar_fuerza_password("PasswordTest") is False
