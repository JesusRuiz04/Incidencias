"""
Tests para el módulo auth_service.
Tests super simples sin clases.
"""

from src.auth_service import (
    validar_email,
    validar_fuerza_password,
    hashear_password,
    crear_usuario
)


# Tests de validar_email
def test_email_valido():
    assert validar_email("juan@ejemplo.com") is True


def test_email_sin_arroba():
    assert validar_email("juansinformato.com") is False


# Tests de validar_fuerza_password
def test_password_fuerte():
    assert validar_fuerza_password("Password123") is True


def test_password_muy_corta():
    assert validar_fuerza_password("Pass1") is False


# Tests de hashear_password
def test_hashear_devuelve_string():
    resultado = hashear_password("mipass")
    assert isinstance(resultado, str)


def test_passwords_diferentes_hashes_diferentes():
    hash1 = hashear_password("pass1")
    hash2 = hashear_password("pass2")
    assert hash1 != hash2


# Tests de crear_usuario
def test_crear_usuario_valido():
    usuario = crear_usuario("Juan", "juan@test.com", "Password123")
    assert usuario is not None
    assert usuario["nombre"] == "Juan"


def test_crear_usuario_email_invalido():
    usuario = crear_usuario("Juan", "juansinformato", "Password123")
    assert usuario is None
