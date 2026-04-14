"""
Tests para analytics.
"""

from src.analytics import contar_por_tipo, contar_por_estado, total_incidencias, incidencias_abiertas, incidencias_cerradas

# Datos de prueba
incidencias = [
    {"tipo": "semaforo", "estado": "abierto"},
    {"tipo": "bache", "estado": "abierto"},
    {"tipo": "semaforo", "estado": "cerrado"}
]

def test_contar_por_tipo():
    resultado = contar_por_tipo(incidencias)
    assert resultado["semaforo"] == 2
    
def test_contar_por_estado():
    assert contar_por_estado(incidencias)["abierto"] == 2
    
def test_total_incidencias():
    assert total_incidencias(incidencias) == 3
    
def test_incidencias_abiertas():
    assert incidencias_abiertas(incidencias) == 2
    
def test_incidencias_cerradas():
    assert incidencias_cerradas(incidencias) == 1
    
def test_contar_por_tipo_vacio():
    assert contar_por_tipo([]) == {}

def test_incidencias_cerradas_ninguna():
    solo_abiertas = [
        {"tipo": "semaforo", "estado": "abierto"},
        {"tipo": "bache", "estado": "abierto"}
    ]
    assert incidencias_cerradas(solo_abiertas) == 0