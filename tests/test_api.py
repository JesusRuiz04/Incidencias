"""
Tests exhaustivos para los endpoints de la API.
Cubre: autenticación, reportes, upload, estadísticas.
"""

from fastapi.testclient import TestClient
from src.main import app
from src.security import create_access_token
from datetime import timedelta
import random
import string

client = TestClient(app)

# Token de prueba
TEST_TOKEN = create_access_token(data={"sub": "1"}, expires_delta=timedelta(hours=1))


def generar_email_aleatorio():
    """Genera un email único para cada test."""
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"test{random_str}@example.com"


# ==================== TESTS DE PÁGINAS ====================

def test_get_index():
    """Test para la página de inicio."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


def test_get_login():
    """Test para la página de login."""
    response = client.get("/login.html")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


def test_get_reporte():
    """Test para la página de crear reporte."""
    response = client.get("/reporte")
    assert response.status_code == 200


def test_get_dashboard():
    """Test para el dashboard."""
    response = client.get("/dashboard")
    assert response.status_code == 200


# ==================== TESTS DE AUTENTICACIÓN ====================

def test_registro_valido():
    """Test para registrar un nuevo usuario con datos válidos."""
    email = generar_email_aleatorio()
    datos = {
        "nombre": "Usuario Test",
        "email": email,
        "password": "TestPass123"
    }
    response = client.post("/api/auth/registro", json=datos)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["usuario"]["email"] == email
    assert data["usuario"]["nombre"] == "Usuario Test"


def test_registro_nombre_corto():
    """Test que falla si el nombre es muy corto."""
    email = generar_email_aleatorio()
    datos = {
        "nombre": "A",
        "email": email,
        "password": "TestPass123"
    }
    response = client.post("/api/auth/registro", json=datos)
    assert response.status_code == 400


def test_registro_email_duplicado():
    """Test que falla si el email ya existe."""
    email = generar_email_aleatorio()
    
    # Primer registro
    datos1 = {
        "nombre": "Usuario 1",
        "email": email,
        "password": "TestPass123"
    }
    response1 = client.post("/api/auth/registro", json=datos1)
    assert response1.status_code == 200
    
    # Intentar registrar con el mismo email
    datos2 = {
        "nombre": "Usuario 2",
        "email": email,
        "password": "TestPass456"
    }
    response2 = client.post("/api/auth/registro", json=datos2)
    assert response2.status_code == 400
    assert "ya está registrado" in response2.json().get("detail", "")


def test_registro_password_debil():
    """Test que falla si la contraseña es débil."""
    email = generar_email_aleatorio()
    datos = {
        "nombre": "Usuario Test",
        "email": email,
        "password": "weak"  # Sin mayúsculas, minúsculas, números
    }
    response = client.post("/api/auth/registro", json=datos)
    assert response.status_code == 400


def test_login_valido():
    """Test para iniciar sesión con credenciales válidas."""
    email = generar_email_aleatorio()
    
    # Primero registrar
    datos_reg = {
        "nombre": "Login Test",
        "email": email,
        "password": "LoginPass123"
    }
    client.post("/api/auth/registro", json=datos_reg)

    # Luego login
    datos_login = {
        "email": email,
        "password": "LoginPass123"
    }
    response = client.post("/api/auth/login", json=datos_login)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["usuario"]["email"] == email


def test_login_password_incorrecta():
    """Test que falla con contraseña incorrecta."""
    email = generar_email_aleatorio()
    
    # Registrar usuario
    datos_reg = {
        "nombre": "Test User",
        "email": email,
        "password": "CorrectPass123"
    }
    client.post("/api/auth/registro", json=datos_reg)
    
    # Intentar login con contraseña incorrecta
    datos_login = {
        "email": email,
        "password": "WrongPass123"
    }
    response = client.post("/api/auth/login", json=datos_login)
    assert response.status_code == 401


def test_login_usuario_inexistente():
    """Test que falla con usuario inexistente."""
    email = generar_email_aleatorio()
    datos = {
        "email": email,
        "password": "AnyPass123"
    }
    response = client.post("/api/auth/login", json=datos)
    assert response.status_code == 401


# ==================== TESTS DE REPORTES ====================

def test_crear_reporte_valido():
    """Test para crear un reporte con datos válidos."""
    datos = {
        "titulo": "Semáforo dañado en esquina",
        "descripcion": "El semáforo no funciona correctamente",
        "ubicacion": "Calle Principal y 5ta Avenida",
        "tipo": "semaforo",
        "prioridad": "alta",
        "estado": "abierto"
    }
    response = client.post(
        "/api/crear-reporte",
        json=datos,
        headers={"Authorization": f"Bearer {TEST_TOKEN}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["mensaje"] == "Reporte creado exitosamente"


def test_crear_reporte_titulo_corto():
    """Test que falla si el título es muy corto."""
    datos = {
        "titulo": "aa",
        "descripcion": "Descripción",
        "ubicacion": "Ubicación válida",
        "tipo": "semaforo",
        "prioridad": "media",
        "estado": "abierto"
    }
    response = client.post(
        "/api/crear-reporte",
        json=datos,
        headers={"Authorization": f"Bearer {TEST_TOKEN}"}
    )
    assert response.status_code == 400


def test_crear_reporte_ubicacion_corta():
    """Test que falla si la ubicación es muy corta."""
    datos = {
        "titulo": "Título válido",
        "descripcion": "Descripción",
        "ubicacion": "ab",
        "tipo": "semaforo",
        "prioridad": "media",
        "estado": "abierto"
    }
    response = client.post(
        "/api/crear-reporte",
        json=datos,
        headers={"Authorization": f"Bearer {TEST_TOKEN}"}
    )
    assert response.status_code == 400


def test_crear_reporte_sin_autenticacion():
    """Test que falla si no hay token."""
    datos = {
        "titulo": "Semáforo dañado",
        "ubicacion": "Calle Principal",
        "tipo": "semaforo",
        "estado": "abierto"
    }
    response = client.post("/api/crear-reporte", json=datos)
    assert response.status_code == 401


def test_crear_reportes_diferentes_tipos():
    """Test para crear reportes de diferentes tipos."""
    tipos = ["semaforo", "bache", "poste", "alcantarilla", "señalizacion", "otro"]
    
    for tipo in tipos:
        datos = {
            "titulo": f"Incidencia de {tipo}",
            "ubicacion": f"Calle {tipo}",
            "tipo": tipo,
            "prioridad": "media",
            "estado": "abierto"
        }
        response = client.post(
            "/api/crear-reporte",
            json=datos,
            headers={"Authorization": f"Bearer {TEST_TOKEN}"}
        )
        assert response.status_code == 200


def test_crear_reportes_diferentes_prioridades():
    """Test para crear reportes con diferentes prioridades."""
    prioridades = ["baja", "media", "alta"]
    
    for prioridad in prioridades:
        datos = {
            "titulo": f"Reporte con prioridad {prioridad}",
            "ubicacion": f"Ubicación {prioridad}",
            "tipo": "semaforo",
            "prioridad": prioridad,
            "estado": "abierto"
        }
        response = client.post(
            "/api/crear-reporte",
            json=datos,
            headers={"Authorization": f"Bearer {TEST_TOKEN}"}
        )
        assert response.status_code == 200


# ==================== TESTS DE LISTADO Y ESTADÍSTICAS ====================

def test_listar_reportes():
    """Test para listar los reportes del usuario."""
    response = client.get(
        "/api/reportes",
        headers={"Authorization": f"Bearer {TEST_TOKEN}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "reportes" in data
    assert "total" in data
    assert isinstance(data["reportes"], list)


def test_listar_reportes_sin_autenticacion():
    """Test que falla si no hay token."""
    response = client.get("/api/reportes")
    assert response.status_code == 401


def test_estadisticas():
    """Test para obtener estadísticas."""
    response = client.get(
        "/api/estadisticas",
        headers={"Authorization": f"Bearer {TEST_TOKEN}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "total_reportes" in data
    assert "por_tipo" in data
    assert "por_estado" in data
    assert "por_prioridad" in data
    assert "reportes_recientes" in data
    assert isinstance(data["reportes_recientes"], list)


def test_estadisticas_sin_autenticacion():
    """Test que falla si no hay token."""
    response = client.get("/api/estadisticas")
    assert response.status_code == 401


def test_estadisticas_estructura():
    """Test que valida la estructura de estadísticas."""
    response = client.get(
        "/api/estadisticas",
        headers={"Authorization": f"Bearer {TEST_TOKEN}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # Validar que son diccionarios
    assert isinstance(data["por_tipo"], dict)
    assert isinstance(data["por_estado"], dict)
    assert isinstance(data["por_prioridad"], dict)
    
    # Validar que tienen valores numéricos
    for valor in data["por_tipo"].values():
        assert isinstance(valor, int)


# ==================== TESTS DE ERRORES GENERALES ====================

def test_endpoint_inexistente():
    """Test para endpoint que no existe."""
    response = client.get("/api/inexistente")
    assert response.status_code == 404


def test_metodo_no_permitido():
    """Test para método HTTP no permitido."""
    response = client.delete("/api/crear-reporte")
    assert response.status_code == 405


def test_respuesta_json_valido():
    """Test que valida que las respuestas sean JSON válido."""
    response = client.get("/")
    # Validar que la respuesta sea HTML
    assert "text/html" in response.headers.get("content-type", "")
    
    # Probar endpoint JSON
    response = client.get(
        "/api/reportes",
        headers={"Authorization": f"Bearer {TEST_TOKEN}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
