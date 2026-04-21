"""
Tests para el módulo models.
"""

from src.models import Usuario, Incidencia

def test_crear_usuario():
    usuario = Usuario(
        nombre="Juan",
        email="juan@test.com",
        password_hash="mipass123"
    )
    assert usuario.nombre == "Juan"
    assert usuario.email == "juan@test.com"
    
    
def test_crear_incidencia():
    incidencia = Incidencia(
        id=1,
        titulo="aaa",
        descripcion="bbb",
        ubicacion="123123",
        tipo="semaforo",
        estado="cerrado",
    )
    assert incidencia.id == 1
    assert incidencia.titulo == "aaa"
    assert incidencia.descripcion == "bbb"
    assert incidencia.ubicacion == "123123"
    assert incidencia.tipo == "semaforo"
    assert incidencia.estado  == "cerrado"

def test_usuario_tiene_atributo_fecha():
    usuario = Usuario(
        nombre="Ana",
        email="ana@test.com",
        password_hash="pass123"
    )
    assert hasattr(usuario, 'fecha_creacion')
    
def test_incidencia_sin_descripcion():
    incidencia = Incidencia(
        titulo="Test",
        ubicacion="Ubicación",
        tipo="semaforo",
        estado="abierto"
    )
    assert incidencia.descripcion is None