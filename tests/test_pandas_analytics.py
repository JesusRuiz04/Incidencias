"""
Tests para funciones de análisis con pandas.
"""

import pytest
from datetime import datetime, timedelta
from src.models import Base, engine, SessionLocal, Usuario, Incidencia
from src.security import hash_password
from src.analytics_pandas import obtener_reportes_por_periodo, obtener_tendencias, exportar_reportes_csv


@pytest.fixture
def setup_test_data():
    """Crear datos de prueba en la BD."""
    Base.metadata.create_all(engine)
    db = SessionLocal()
    
    # Limpiar
    db.query(Incidencia).delete()
    db.query(Usuario).delete()
    db.commit()
    
    # Crear usuario
    usuario = Usuario(
        nombre="Test User",
        email="test@example.com",
        password_hash=hash_password("TestPass123"),
        fecha_creacion=datetime.now()
    )
    db.add(usuario)
    db.commit()
    
    # Crear reportes
    for i in range(10):
        reporte = Incidencia(
            titulo=f"Reporte {i+1}",
            descripcion=f"Descripción {i+1}",
            ubicacion=f"Ubicación {i+1}",
            tipo="semaforo" if i % 2 == 0 else "bache",
            estado="abierto" if i % 3 == 0 else ("en_progreso" if i % 3 == 1 else "cerrado"),
            prioridad="alta" if i % 2 == 0 else "baja",
            fotos="",
            usuario_id=usuario.id,
            fecha_creacion=datetime.now() - timedelta(days=i)
        )
        db.add(reporte)
    
    db.commit()
    yield usuario, db
    
    # Cleanup
    db.query(Incidencia).delete()
    db.query(Usuario).delete()
    db.commit()
    db.close()


def test_obtener_reportes_por_periodo_semanal(setup_test_data):
    """Test análisis semanal con pandas."""
    usuario, db = setup_test_data
    
    resultado = obtener_reportes_por_periodo(usuario.id, "semanal")
    
    assert resultado["periodo"] == "semanal"
    assert resultado["total_reportes"] == 10
    assert resultado["promedio_por_periodo"] > 0
    assert len(resultado["por_periodo"]) > 0
    assert resultado["tipo_mas_comun"] in ["semaforo", "bache"]


def test_obtener_reportes_por_periodo_mensual(setup_test_data):
    """Test análisis mensual con pandas."""
    usuario, db = setup_test_data
    
    resultado = obtener_reportes_por_periodo(usuario.id, "mensual")
    
    assert resultado["periodo"] == "mensual"
    assert resultado["total_reportes"] == 10
    assert resultado["label_periodo"] == "Mes"


def test_obtener_tendencias(setup_test_data):
    """Test análisis de tendencias con pandas."""
    usuario, db = setup_test_data
    
    resultado = obtener_tendencias(usuario.id, 30)
    
    assert resultado["dias"] == 30
    assert resultado["total_reportes"] == 10
    assert resultado["velocidad_resolucion_pct"] >= 0
    assert len(resultado["por_dia"]) > 0


def test_exportar_reportes_csv(setup_test_data):
    """Test exportación a CSV con pandas."""
    usuario, db = setup_test_data
    
    df = exportar_reportes_csv(usuario.id)
    
    assert len(df) == 10
    assert "ID" in df.columns
    assert "Título" in df.columns
    assert "Estado" in df.columns


def test_reportes_vacio(setup_test_data):
    """Test cuando no hay reportes."""
    usuario, db = setup_test_data
    
    # Crear usuario sin reportes
    usuario2 = Usuario(
        nombre="Empty User",
        email="empty@example.com",
        password_hash=hash_password("EmptyPass123"),
        fecha_creacion=datetime.now()
    )
    db.add(usuario2)
    db.commit()
    
    resultado = obtener_reportes_por_periodo(usuario2.id, "semanal")
    
    assert resultado["total_reportes"] == 0
    assert resultado["por_periodo"] == []
    assert resultado["tipo_mas_comun"] is None


def test_tendencias_recientes(setup_test_data):
    """Test tendencias recientes (últimos 7 días)."""
    usuario, db = setup_test_data
    
    resultado = obtener_tendencias(usuario.id, 7)
    
    assert resultado["dias"] == 7
    # Puede ser 0 o más según los reportes
    assert resultado["total_reportes"] >= 0
