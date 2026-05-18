"""
Modelos de datos simplificados.
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Configuración base de datos
DATABASE_URL = "sqlite:///data/incidencias.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Usuario(Base):
    """Modelo de Usuario."""
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    es_admin = Column(Integer, default=0)  # 0 = usuario normal, 1 = admin
    fecha_creacion = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<Usuario(nombre='{self.nombre}', email='{self.email}', es_admin={self.es_admin})>"


class Incidencia(Base):
    """Modelo de Incidencia."""
    __tablename__ = "incidencias"
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(String(500))
    ubicacion = Column(String(200), nullable=False)
    tipo = Column(String(50), nullable=False)  # semaforo, bache, poste, etc
    estado = Column(String(50), nullable=False)  # abierto, cerrado, en_progreso
    prioridad = Column(String(20), default="media")  # baja, media, alta
    fotos = Column(String(500))  # URLs de fotos separadas por comas
    usuario_id = Column(Integer)  # ID del usuario que creó la incidencia
    fecha_creacion = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<Incidencia(titulo='{self.titulo}', tipo='{self.tipo}', estado='{self.estado}')>"


# Crear tablas
Base.metadata.create_all(engine)
