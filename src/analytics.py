"""
Módulo para análisis de datos de incidencias.
Funciones simples para contar y analizar datos.
"""


def contar_por_tipo(incidencias):
    """Cuenta cuántas incidencias hay de cada tipo."""
    tipos = {}
    
    for incidencia in incidencias:
        tipo = incidencia["tipo"]
        if tipo in tipos:
            tipos[tipo] = tipos[tipo] + 1
        else:
            tipos[tipo] = 1
    
    return tipos


def contar_por_estado(incidencias):
    """Cuenta cuántas incidencias hay por cada estado."""
    estados = {}
    
    for incidencia in incidencias:
        estado = incidencia["estado"]
        if estado in estados:
            estados[estado] = estados[estado] + 1
        else:
            estados[estado] = 1
    
    return estados


def total_incidencias(incidencias):
    """Retorna el total de incidencias."""
    return len(incidencias)


def incidencias_abiertas(incidencias):
    """Retorna cuántas incidencias están abiertas."""
    contador = 0
    for incidencia in incidencias:
        if incidencia["estado"] == "abierto":
            contador = contador + 1
    return contador


def incidencias_cerradas(incidencias):
    """Retorna cuántas incidencias están cerradas."""
    contador = 0
    for incidencia in incidencias:
        if incidencia["estado"] == "cerrado":
            contador = contador + 1
    return contador
