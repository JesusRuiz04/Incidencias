"""
Script para llenar la base de datos con datos de ejemplo.
Ejecutar: python seed_db.py
"""

from src.models import Base, engine, SessionLocal, Usuario, Incidencia
from src.security import hash_password
from datetime import datetime, timedelta
import os
from pathlib import Path

def create_sample_images():
    """Crea imágenes de ejemplo para los reportes."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import random
        
        uploads_dir = Path("static/uploads")
        uploads_dir.mkdir(parents=True, exist_ok=True)
        
        # Colores para las imágenes
        colors = [
            "#FF6B6B",  # Rojo
            "#4ECDC4",  # Turquesa
            "#45B7D1",  # Azul
            "#FFA502",  # Naranja
            "#6BCF7F",  # Verde
            "#FFE66D",  # Amarillo
        ]
        
        image_paths = []
        
        # Crear 6 imágenes de ejemplo
        for i in range(6):
            width, height = 400, 300
            color = colors[i % len(colors)]
            # Convertir hex a RGB
            color_rgb = tuple(int(color.lstrip('#')[j:j+2], 16) for j in (0, 2, 4))
            
            img = Image.new('RGB', (width, height), color_rgb)
            draw = ImageDraw.Draw(img)
            
            # Agregar texto
            text = f"Imagen de Ejemplo {i+1}"
            text_position = (width // 2, height // 2)
            
            try:
                draw.text(text_position, text, fill=(255, 255, 255), anchor="mm")
            except:
                # Si falla la fuente, solo dejar el color
                pass
            
            # Guardar imagen
            filename = f"sample_image_{i+1}.png"
            filepath = uploads_dir / filename
            img.save(filepath)
            
            image_paths.append(f"/static/uploads/{filename}")
            print(f"   ✅ Imagen creada: {filename}")
        
        return image_paths
    except ImportError:
        print("   ⚠️  PIL no está instalado, usando URLs de placeholder")
        # Usar imágenes placeholder de internet como fallback
        return [
            "https://via.placeholder.com/400x300/FF6B6B/FFFFFF?text=Incidencia+1",
            "https://via.placeholder.com/400x300/4ECDC4/FFFFFF?text=Incidencia+2",
            "https://via.placeholder.com/400x300/45B7D1/FFFFFF?text=Incidencia+3",
            "https://via.placeholder.com/400x300/FFA502/FFFFFF?text=Incidencia+4",
            "https://via.placeholder.com/400x300/6BCF7F/FFFFFF?text=Incidencia+5",
            "https://via.placeholder.com/400x300/FFE66D/333333?text=Incidencia+6",
        ]

def seed_database():
    """Crea datos de ejemplo en la base de datos."""
    
    # Crear tablas si no existen
    Base.metadata.create_all(engine)
    
    # Crear imágenes de ejemplo
    print("\n📸 Creando imágenes de ejemplo...")
    image_paths = create_sample_images()
    
    db = SessionLocal()
    
    try:
        # Limpiar datos existentes (opcional)
        db.query(Incidencia).delete()
        db.query(Usuario).delete()
        db.commit()
        
        # Crear usuarios de ejemplo
        usuario1 = Usuario(
            nombre="Juan Pérez",
            email="juan@example.com",
            password_hash=hash_password("Password123"),
            es_admin=1,  # Admin user
            fecha_creacion=datetime.now()
        )
        
        usuario2 = Usuario(
            nombre="María García",
            email="maria@example.com",
            password_hash=hash_password("Password456"),
            es_admin=0,  # Regular user
            fecha_creacion=datetime.now()
        )
        
        db.add(usuario1)
        db.add(usuario2)
        db.commit()
        
        print("✅ Usuarios creados:")
        print(f"   - {usuario1.nombre} ({usuario1.email}) - {'👑 ADMIN' if usuario1.es_admin else 'Usuario'}")
        print(f"   - {usuario2.nombre} ({usuario2.email}) - {'👑 ADMIN' if usuario2.es_admin else 'Usuario'}")
        
        # Crear reportes de ejemplo con imágenes
        reportes = [
            Incidencia(
                titulo="Semáforo dañado en intersección",
                descripcion="El semáforo no funciona correctamente, mantiene luz roja constantemente.",
                ubicacion="Calle Principal y 5ta Avenida",
                tipo="semaforo",
                estado="abierto",
                prioridad="alta",
                fotos=image_paths[0],
                usuario_id=usuario1.id,
                fecha_creacion=datetime.now() - timedelta(days=5)
            ),
            Incidencia(
                titulo="Bache grande en la carretera",
                descripcion="Hay un bache considerable que causa daño a los vehículos.",
                ubicacion="Carretera Sur, km 3.5",
                tipo="bache",
                estado="en_progreso",
                prioridad="alta",
                fotos=image_paths[1],
                usuario_id=usuario1.id,
                fecha_creacion=datetime.now() - timedelta(days=3)
            ),
            Incidencia(
                titulo="Poste inclinado",
                descripcion="Un poste de electricidad se está inclinando peligrosamente.",
                ubicacion="Avenida Central 2do cuadra",
                tipo="poste",
                estado="abierto",
                prioridad="media",
                fotos=image_paths[2],
                usuario_id=usuario2.id,
                fecha_creacion=datetime.now() - timedelta(days=2)
            ),
            Incidencia(
                titulo="Alcantarilla destapada",
                descripcion="La alcantarilla perdió la tapa, representa peligro.",
                ubicacion="Barrio Este, calle 8",
                tipo="alcantarilla",
                estado="en_progreso",
                prioridad="alta",
                fotos=image_paths[3],
                usuario_id=usuario2.id,
                fecha_creacion=datetime.now() - timedelta(days=4)
            ),
            Incidencia(
                titulo="Señalización faltante",
                descripcion="Falta señalización en la curva peligrosa.",
                ubicacion="Ruta Principal, km 15",
                tipo="señalizacion",
                estado="cerrado",
                prioridad="media",
                fotos=image_paths[4],
                usuario_id=usuario1.id,
                fecha_creacion=datetime.now() - timedelta(days=10)
            ),
            Incidencia(
                titulo="Otro problema de tráfico",
                descripcion="Acumulación de agua en la calle por drenaje deficiente.",
                ubicacion="Zona comercial Sur",
                tipo="otro",
                estado="abierto",
                prioridad="baja",
                fotos=image_paths[5],
                usuario_id=usuario2.id,
                fecha_creacion=datetime.now() - timedelta(days=1)
            ),
            Incidencia(
                titulo="Semáforo apagado",
                descripcion="El semáforo se apaga a cierta hora del día.",
                ubicacion="Intersección Centro",
                tipo="semaforo",
                estado="cerrado",
                prioridad="media",
                fotos="",
                usuario_id=usuario1.id,
                fecha_creacion=datetime.now() - timedelta(days=7)
            ),
            Incidencia(
                titulo="Acera destruida",
                descripcion="La acera tiene grietas profundas y es peligrosa.",
                ubicacion="Calle de los Rosales",
                tipo="otro",
                estado="abierto",
                prioridad="media",
                fotos=",".join([image_paths[0], image_paths[1]]),
                usuario_id=usuario2.id,
                fecha_creacion=datetime.now() - timedelta(hours=6)
            ),
        ]
        
        for reporte in reportes:
            db.add(reporte)
        
        db.commit()
        
        print("\n✅ Reportes creados:")
        for i, reporte in enumerate(reportes, 1):
            fotos_count = len([f for f in reporte.fotos.split(',') if f.strip()]) if reporte.fotos else 0
            print(f"   {i}. {reporte.titulo} ({reporte.tipo}) - Estado: {reporte.estado} - 📸 {fotos_count} foto(s)")
        
        # Estadísticas
        total_reportes = db.query(Incidencia).count()
        abiertos = db.query(Incidencia).filter(Incidencia.estado == "abierto").count()
        en_progreso = db.query(Incidencia).filter(Incidencia.estado == "en_progreso").count()
        cerrados = db.query(Incidencia).filter(Incidencia.estado == "cerrado").count()
        
        print(f"\n📊 Estadísticas:")
        print(f"   Total reportes: {total_reportes}")
        print(f"   Abiertos: {abiertos}")
        print(f"   En progreso: {en_progreso}")
        print(f"   Cerrados: {cerrados}")
        
        print("\n✅ Base de datos poblada correctamente!")
        print("\n🔐 Credenciales de prueba:")
        print("   Usuario 1 (ADMIN): juan@example.com / Password123")
        print("   Usuario 2 (Regular): maria@example.com / Password456")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error al poblar la BD: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
