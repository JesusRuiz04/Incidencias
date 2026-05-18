"""
Tests para el módulo auth_service.
Tests super simples sin clases.
"""

from src.auth_service import (
    validar_email,
    validar_fuerza_password,
)

def test_email_valido():
    assert validar_email("juan@ejemplo.com") is True




def test_password_fuerte():
    assert validar_fuerza_password("Password123") is True


def test_password_muy_corta():
    assert validar_fuerza_password("Pass1") is False


def test_password_sin_mayuscula():
    assert validar_fuerza_password("password123") is False


def test_password_sin_minuscula():
    assert validar_fuerza_password("PASSWORD123") is False


def test_password_sin_numero():
    assert validar_fuerza_password("PasswordTest") is False
