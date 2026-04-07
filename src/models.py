"""
Modelos de datos simplificados.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración base de datos
DATABASE_URL = "sqlite:///incidencias.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# Crear tablas
Base.metadata.create_all(engine)


