# Sistema de Incidencias de Tráfico - Testing con Pytest

Proyecto de testing para un sistema de gestión de incidencias de tráfico usando pytest.

## Estructura del Proyecto

ProyectoFinal/
├── src/
│   ├── auth_service.py      - Servicios de autenticación
│   ├── analytics.py         - Análisis de datos
│   ├── models.py            - Modelos de datos
│   └── main.py              - API FastAPI
├── tests/
│   ├── test_auth_service.py - Tests de autenticación
│   ├── test_analytics.py    - Tests de análisis
│   └── __init__.py
├── pytest.ini               - Configuración de pytest
└── requisitos.txt           - Dependencias

## Instalación

1. Activa el entorno virtual:
   .\.venv\Scripts\Activate.ps1

2. Instala las dependencias:
   pip install -r requisitos.txt

## Ejecutar Tests

Todos los tests:
  python -m pytest

Tests específicos:
  python -m pytest tests/test_auth_service.py
  python -m pytest tests/test_analytics.py


## Tests Disponibles

### auth_service.py 
- Validación de email
- Validación de fuerza de contraseña
- Hasheo de contraseñas
- Creación de usuarios

### analytics.py 
- Contar incidencias por tipo
- Contar incidencias por estado
- Total de incidencias
- Incidencias abiertas
- Incidencias cerradas

## Módulos

### auth_service.py
Funciones para validación y gestión de usuarios:
- validar_email()
- validar_fuerza_password()
- hashear_password()
- crear_usuario()

### analytics.py
Funciones para análisis de datos de incidencias:
- contar_por_tipo()
- contar_por_estado()
- total_incidencias()
- incidencias_abiertas()
- incidencias_cerradas()