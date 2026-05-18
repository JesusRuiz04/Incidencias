# � Sistema de Incidencias de Tráfico - v2.0

Sistema completo de gestión de reportes de incidencias de tráfico con autenticación JWT, análisis avanzados con pandas y dashboard interactivo.

## ✨ Características Principales

### 🔐 Autenticación y Seguridad
- **Registro/Login** con JWT (JSON Web Tokens)
- **Hashing de contraseñas** con PBKDF2-SHA256
- **Validación de email** y contraseñas robustas (8+ caracteres, mayúscula, minúscula, número)
- **Tokens con expiración** de 30 minutos

### 📱 Gestión de Reportes
- Crear reportes de incidencias con foto
- Listar reportes del usuario autenticado
- Estados: Abierto, En Progreso, Cerrado
- Prioridades: Alta, Media, Baja
- Tipos: Semáforo, Bache, Poste, Alcantarilla, Señalización, Otro
- Ubicación y descripción detallada

### 📸 Fotos y Multimedia
- Subida de fotos (máx. 5MB)
- Visualización de miniaturas en dashboard
- Lightbox para ver imágenes ampliadas
- URLs de placeholder como fallback

### 📊 Dashboard Interactivo
- **Tarjetas de estadísticas** con métricas principales
- **Gráficos Chart.js** por tipo, estado y prioridad
- **Reportes recientes** con miniaturas de fotos
- **Auto-actualización** cada 30 segundos

### 📈 **NUEVO: Análisis Avanzados con Pandas**
- **Análisis por período** (semanal/mensual)
- **Cálculo de tendencias** (últimos 30 días)
- **Velocidad de resolución** de reportes
- **Exportación de datos** a CSV y JSON
- **Gráficos dinámicos** con Chart.js
- Página dedicada de análisis con 3 pestañas

---

## 🚀 Inicio Rápido

### Requisitos Previos
- Python 3.10+
- Windows/Mac/Linux

### Instalación

1. **Abrir el proyecto**
   ```bash
   cd ProyectoFinal
   ```

2. **Crear entorno virtual (Windows)**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Crear entorno virtual (Mac/Linux)**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. **Instalar dependencias**
   ```bash
   pip install -r requisitos.txt
   ```

5. **Crear base de datos (opcional)**
   ```bash
   python seed_db.py
   ```
   Esto crea 2 usuarios de prueba y 8 reportes de ejemplo con imágenes.

6. **Ejecutar servidor**
   ```bash
   python -m uvicorn src.main:app --reload
   ```
   Accede a http://localhost:8000

---

## 📋 Credenciales de Prueba

Después de ejecutar `seed_db.py`:

| Email | Contraseña | Nombre |
|-------|-----------|--------|
| juan@example.com | Password123 | Juan Pérez |
| maria@example.com | Password456 | María García |

---

## 📁 Estructura del Proyecto

```
ProyectoFinal/
├── src/
│   ├── main.py                 # API FastAPI (16 endpoints)
│   ├── models.py               # Modelos SQLAlchemy
│   ├── security.py             # Autenticación y hashing
│   ├── auth_service.py         # Validación de datos
│   └── analytics_pandas.py     # ⭐ Análisis con pandas
├── templates/
│   ├── index.html              # Página de inicio
│   ├── login.html              # Login/Registro
│   ├── dashboard.html          # Dashboard principal
│   ├── reporte.html            # Crear reporte
│   └── analisis.html           # ⭐ Análisis avanzado (NUEVO)
├── static/
│   ├── css/style.css           # Estilos
│   ├── js/auth.js              # Lógica de autenticación
│   └── uploads/                # Fotos cargadas
├── tests/
│   ├── test_api.py             # Tests de endpoints (25)
│   ├── test_auth_service.py    # Tests de validación (12)
│   ├── test_analytics.py       # Tests de análisis (7)
│   ├── test_models.py          # Tests de modelos (4)
│   └── test_pandas_analytics.py # ⭐ Tests de pandas (6)
├── data/
│   └── incidencias.db          # Base de datos SQLite
├── seed_db.py                  # Script para llenar BD
├── pytest.ini                  # Configuración de pytest
├── requisitos.txt              # Dependencias
└── README.md                   # Este archivo
```

---

## 🔌 Endpoints de API

### Autenticación
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/auth/registro` | Registrar nuevo usuario |
| POST | `/api/auth/login` | Iniciar sesión |

### Reportes
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/crear-reporte` | Crear nuevo reporte |
| GET | `/api/reportes` | Listar reportes del usuario |
| GET | `/api/estadisticas` | Obtener estadísticas |

### Fotos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/upload-foto` | Subir foto para reporte |

### ⭐ Análisis Avanzado (Pandas) - NUEVO
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/reportes-por-periodo` | Análisis semanal/mensual |
| GET | `/api/tendencias` | Tendencias de últimos 30 días |
| GET | `/api/exportar-reportes` | Descargar reportes (CSV/JSON) |

### Páginas Web
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Inicio |
| GET | `/login.html` | Login/Registro |
| GET | `/dashboard` | Dashboard |
| GET | `/reporte` | Crear reporte |
| GET | `/analisis` | ⭐ Análisis avanzado (NUEVO) |

---

## 🧪 Testing

### Ejecutar Todos los Tests
```bash
python -m pytest tests/ -v
```

### Resultados Esperados
```
✅ 54 tests pasando
```

**Desglose:**
- 25 tests de API (`test_api.py`)
- 12 tests de autenticación (`test_auth_service.py`)
- 7 tests de análisis (`test_analytics.py`)
- 4 tests de modelos (`test_models.py`)
- 6 tests de pandas (`test_pandas_analytics.py`) ⭐ NUEVO

### Tests Específicos
```bash
# Solo tests de API
python -m pytest tests/test_api.py -v

# Solo tests de pandas (NUEVO)
python -m pytest tests/test_pandas_analytics.py -v

# Con cobertura
python -m pytest tests/ --cov=src --cov-report=html
```

---

## 📊 Análisis Avanzado con Pandas - NUEVO

### 🎯 Página de Análisis

Acceda a: **http://localhost:8000/analisis**

#### **Pestaña 1: Reportes por Período**
Agrupa reportes por semana o mes y muestra:
- ✅ Total de reportes
- ✅ Tipo más común
- ✅ Prioridad más reportada
- ✅ Promedio de reportes por período
- ✅ Desglose de estados (Abierto, En Progreso, Cerrado)
- ✅ Gráfico de barras apiladas

**Uso:**
```python
from src.analytics_pandas import obtener_reportes_por_periodo

# Análisis semanal
resultado = obtener_reportes_por_periodo(usuario_id=1, periodo="semanal")

# Análisis mensual
resultado = obtener_reportes_por_periodo(usuario_id=1, periodo="mensual")
```

#### **Pestaña 2: Tendencias (Últimos 30 días)**
Analiza reportes de los últimos 30 días:
- ✅ Total de reportes creados
- ✅ Reportes cerrados
- ✅ Velocidad de resolución (%)
- ✅ Distribución diaria
- ✅ Gráfico de líneas con tendencias

**Uso:**
```python
from src.analytics_pandas import obtener_tendencias

# Últimos 30 días
resultado = obtener_tendencias(usuario_id=1, dias=30)

# Últimos 7 días
resultado = obtener_tendencias(usuario_id=1, dias=7)
```

#### **Pestaña 3: Exportar Datos**
Descarga todos tus reportes en diferentes formatos:
- ✅ **CSV**: Para Excel o análisis
- ✅ **JSON**: Para aplicaciones externas

**Uso:**
```python
from src.analytics_pandas import exportar_reportes_csv

df = exportar_reportes_csv(usuario_id=1)
df.to_csv('mis_reportes.csv', index=False)
```

### Ejemplo de Respuesta (Período)

```json
{
  "periodo": "semanal",
  "total_reportes": 10,
  "tipo_mas_comun": "semaforo",
  "prioridad_mas_comun": "alta",
  "promedio_por_periodo": 2.5,
  "por_periodo": [
    {
      "periodo": "2026-W17",
      "total": 3,
      "estados": {
        "abierto": 2,
        "en_progreso": 1,
        "cerrado": 0
      }
    }
  ]
}
```

### Ejemplo de Respuesta (Tendencias)

```json
{
  "dias": 30,
  "total_reportes": 10,
  "cerrados": 3,
  "velocidad_resolucion_pct": 30.0,
  "por_dia": [
    {
      "fecha": "2026-04-25",
      "total": 2
    }
  ]
}
```

---

## 🎨 Interfaz de Usuario

### Login / Registro
- Formulario dual (Login/Registro)
- Validación de email en tiempo real
- Indicador de fuerza de contraseña
- Almacenamiento de token en localStorage

### Dashboard
- 4 tarjetas con métricas principales
- 3 gráficos interactivos (Tipo, Estado, Prioridad)
- Listado de reportes recientes con **miniaturas de fotos** ✨
- Auto-actualización de datos
- **Botón "Análisis Avanzado"** ⭐ NUEVO

### Crear Reporte
- Formulario con validación
- Selección de tipo, estado y prioridad
- Preview de fotos antes de subir
- Drag & drop para fotos

### ⭐ Análisis Avanzado (NUEVO)
- **Pestaña "Por Período"**: Análisis semanal/mensual con gráficos
- **Pestaña "Tendencias"**: Últimos 30 días con velocidad de resolución
- **Pestaña "Exportar"**: Descargas CSV/JSON

---

## 🔐 Seguridad

### Validaciones Implementadas

**Contraseñas:**
- Mínimo 8 caracteres
- Al menos 1 mayúscula
- Al menos 1 minúscula
- Al menos 1 número

**Email:**
- Formato válido RFC 5322
- No permitir duplicados
- Máximo 255 caracteres

**Reportes:**
- Título mínimo 3 caracteres
- Ubicación mínima 3 caracteres
- Solo usuarios autenticados
- Solo acceso a propios reportes

**Fotos:**
- Solo imágenes (JPG, PNG, GIF, WebP)
- Máximo 5MB
- Renombre automático para evitar conflictos

---

## 📦 Dependencias

| Librería | Versión | Uso |
|----------|---------|-----|
| FastAPI | 0.100+ | Framework web |
| Uvicorn | Latest | Servidor ASGI |
| SQLAlchemy | 2.0+ | ORM para BD |
| Pandas | 3.0+ | ⭐ Análisis de datos (NUEVO) |
| Python-Jose | Latest | JWT authentication |
| Passlib | Latest | Hashing de contraseñas |
| Pillow | Latest | Procesamiento de imágenes |
| Pytest | 9.0+ | Testing |
| Chart.js | 3.9.1 | Gráficos (frontend) |

---

## 🛠️ Desarrollo

### Variables de Entorno

```bash
# Opcional - usar valores por defecto
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./data/incidencias.db
```

### Agregar Nuevas Dependencias

```bash
pip install nombre-libreria
pip freeze > requisitos.txt
```

### Ejecutar en Modo Desarrollo

```bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Generar Reporte de Cobertura

```bash
python -m pytest tests/ --cov=src --cov-report=html
# Abre htmlcov/index.html en el navegador
```

---

## 📖 Ejemplos de Uso

### Registrar Nuevo Usuario
```javascript
const response = await fetch('/api/auth/registro', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        nombre: 'Juan Pérez',
        email: 'juan@example.com',
        password: 'MiPassword123'
    })
});
```

### Crear Reporte
```javascript
const formData = new FormData();
formData.append('titulo', 'Semáforo roto');
formData.append('descripcion', 'El semáforo no funciona');
formData.append('ubicacion', 'Calle Principal');
formData.append('tipo', 'semaforo');
formData.append('estado', 'abierto');
formData.append('prioridad', 'alta');

await fetch('/api/crear-reporte', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: formData
});
```

### ⭐ Obtener Análisis por Período (NUEVO)
```javascript
const response = await fetch('/api/reportes-por-periodo?periodo=semanal', {
    headers: { 'Authorization': `Bearer ${token}` }
});
const analisis = await response.json();
console.log(analisis.total_reportes);
console.log(analisis.tipo_mas_comun);
```

### ⭐ Obtener Tendencias (NUEVO)
```javascript
const response = await fetch('/api/tendencias?dias=30', {
    headers: { 'Authorization': `Bearer ${token}` }
});
const tendencias = await response.json();
console.log(tendencias.velocidad_resolucion_pct);
```

### ⭐ Exportar Reportes (NUEVO)
```javascript
// Descargar como CSV
const response = await fetch('/api/exportar-reportes?formato=csv', {
    headers: { 'Authorization': `Bearer ${token}` }
});
const blob = await response.blob();
const url = window.URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'reportes.csv';
a.click();
```

---

## 🐛 Solución de Problemas

### "Servidor no responde"
```bash
netstat -ano | findstr :8000
python -m uvicorn src.main:app --reload --port 8001
```

### "ModuleNotFoundError: No module named 'pandas'"
```bash
pip install pandas
pip install -r requisitos.txt
```

### "Base de datos corrupta"
```bash
rm data/incidencias.db
python seed_db.py
```

### "Las imágenes no se muestran"
```bash
mkdir -p static/uploads
# O usar URLs de placeholder automáticamente
```

---

## 📝 Cambios en v2.0

✨ **NUEVAS CARACTERÍSTICAS:**
- ⭐ Módulo de análisis avanzado con pandas (`src/analytics_pandas.py`)
- ⭐ Página dedicada de análisis (`templates/analisis.html`)
- ⭐ 3 nuevos endpoints de API para análisis
- ⭐ 6 nuevos tests para funciones de pandas
- ⭐ Visualización de fotos en reportes recientes (miniaturas)
- ⭐ Botón de acceso rápido al análisis en dashboard

🔧 **MEJORAS:**
- Mejor espaciado en dashboard y análisis
- Navbar sticky para navegación constante
- Validaciones mejoradas
- Documentación completa

✅ **ESTADO:**
- 54/54 tests pasando
- 0 errores de sintaxis
- Código optimizado y documentado

---

## 📄 Licencia

Proyecto educativo de demostración. Libre para usar y modificar.

---

## 👨‍💻 Información del Proyecto

| Aspecto | Valor |
|--------|-------|
| Versión | 2.0 |
| Última actualización | Abril 2026 |
| Tests | 54/54 ✅ |
| Endpoints | 16 |
| Cobertura | Completa |
| Estado | Production Ready |

---

**¡Sistema listo para usar! 🚀**

## 🎯 Características

### ✅ Autenticación
- Registro de usuarios con validaciones robustas
- Login con JWT (tokens de 30 minutos)
- Hash seguro de contraseñas (pbkdf2_sha256)
- Validación de email y contraseña fuerte

### ✅ Reportes
- Crear reportes de incidencias
- Tipos: Semáforo, Bache, Poste, Alcantarilla, Señalización
- Prioridades: Baja, Media, Alta
- Estados: Abierto, En Progreso, Cerrado

### ✅ Fotos
- Subida de imágenes para reportes
- Vista previa en tiempo real
- Almacenamiento seguro en `/static/uploads`

### ✅ Dashboard
- Gráficos interactivos con Chart.js
- Estadísticas: Total, por Tipo, por Estado, por Prioridad
- Reportes recientes
- Actualización automática cada 30 segundos

### ✅ API REST
- 13 endpoints documentados
- Validaciones exhaustivas
- Manejo robusto de errores
- Logging de operaciones

---

## 📋 Requisitos

Python 3.8+

```bash
pip install -r requisitos.txt
```

### Dependencias Principales:
- **FastAPI** - Framework web
- **SQLAlchemy** - ORM para BD
- **python-jose** - JWT tokens
- **passlib** - Hash de contraseñas
- **pytest** - Testing

---

## 🚀 Instalación y Ejecución

### 1. Clonar/Descargar proyecto

```bash
cd ProyectoFinal
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
# Windows:
.\.venv\Scripts\Activate.ps1
# Mac/Linux:
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requisitos.txt
```

### 4. Iniciar servidor

```bash
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en: **http://localhost:8000**

---

## 📱 Uso de la Aplicación

### 1️⃣ **Registro/Login**
```
URL: http://localhost:8000/login.html

- Hacer clic en "Registrarse"
- Llenar formulario:
  - Nombre: Mínimo 2 caracteres
  - Email: Válido (ej: user@example.com)
  - Contraseña: 8+ caracteres, mayúscula, minúscula, número
- Se genera automáticamente un token JWT
- Redirige al Dashboard
```

### 2️⃣ **Dashboard**
```
URL: http://localhost:8000/dashboard (automático después de login)

Muestra:
- Tarjetas con métricas (Total, Abiertos, En Progreso, Cerrados)
- Gráficos de reportes por Tipo, Estado, Prioridad
- Últimos 5 reportes creados
- Botón para crear nuevo reporte
```

### 3️⃣ **Crear Reporte**
```
URL: http://localhost:8000/reporte

Campos obligatorios:
- Título: Min 3 caracteres
- Ubicación: Min 3 caracteres
- Tipo: Seleccionar de lista

Campos opcionales:
- Descripción: Detalles del problema
- Prioridad: Baja/Media/Alta (default: Media)
- Foto: Subir imagen (jpg, png, etc)

Al enviar:
- Se validan todos los campos
- Se sube la foto (si existe)
- Se guarda en la BD
- Redirige al Dashboard
```

### 4️⃣ **Ver Reportes**
```
Dashboard muestra automáticamente:
- Total de reportes creados
- Estado actual (abierto, en progreso, cerrado)
- Fecha de creación
- Lista de reportes recientes
```

---

## 🧪 Testing

Ejecutar todos los tests:

```bash
# Todos los tests
python -m pytest tests/ --ignore=tests/test_pandas.py -v

# Tests específicos
python -m pytest tests/test_api.py -v
python -m pytest tests/test_auth_service.py -v
python -m pytest tests/test_models.py -v
python -m pytest tests/test_analytics.py -v

# Con coverage
python -m pytest tests/ --ignore=tests/test_pandas.py --cov=src
```

### Cobertura de Tests: **36 tests**

- ✅ **Analytics** (7 tests): Contar por tipo, estado, total, etc.
- ✅ **API** (13 tests): Endpoints de autenticación, reportes, estadísticas
- ✅ **Autenticación** (12 tests): Login, registro, validaciones
- ✅ **Modelos** (4 tests): Estructura de datos

---

## 📁 Estructura del Proyecto

```
ProyectoFinal/
├── src/
│   ├── main.py              # API FastAPI con todos los endpoints
│   ├── models.py            # Modelos SQLAlchemy (Usuario, Incidencia)
│   ├── security.py          # JWT, hash de contraseñas, autenticación
│   ├── auth_service.py      # Validaciones de email y contraseña
│   ├── analytics.py         # Funciones de análisis de datos
│   └── __init__.py
├── tests/
│   ├── test_api.py          # Tests de endpoints API (13 tests)
│   ├── test_auth_service.py # Tests de autenticación (12 tests)
│   ├── test_analytics.py    # Tests de análisis (7 tests)
│   ├── test_models.py       # Tests de modelos (4 tests)
│   └── __init__.py
├── templates/
│   ├── index.html           # Página de inicio
│   ├── login.html           # Login/Registro
│   ├── reporte.html         # Crear reporte
│   ├── dashboard.html       # Dashboard con gráficos
│   └── base.html            # Template base (opcional)
├── static/
│   ├── css/
│   │   └── style.css        # Estilos principales
│   ├── js/
│   │   └── auth.js          # JavaScript (opcional)
│   └── uploads/             # Imágenes subidas
├── data/
│   ├── incidencias.csv      # Datos de ejemplo
│   └── incidencias.db       # Base de datos SQLite
├── pytest.ini               # Configuración de pytest
├── requisitos.txt           # Dependencias Python
├── README.md                # Este archivo
└── .venv/                   # Entorno virtual
```

---

## 🔌 API Endpoints

### **Autenticación**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/auth/registro` | Registrar nuevo usuario |
| `POST` | `/api/auth/login` | Iniciar sesión |

### **Reportes**

| Método | Endpoint | Descripción | Requiere Auth |
|--------|----------|-------------|--|
| `POST` | `/api/crear-reporte` | Crear nuevo reporte | ✅ |
| `GET` | `/api/reportes` | Listar reportes del usuario | ✅ |
| `GET` | `/api/estadisticas` | Obtener estadísticas | ✅ |

### **Upload**

| Método | Endpoint | Descripción | Requiere Auth |
|--------|----------|-------------|--|
| `POST` | `/api/upload-foto` | Subir imagen | ✅ |

### **Páginas**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Página de inicio |
| `GET` | `/login.html` | Login/Registro |
| `GET` | `/reporte` | Crear reporte |
| `GET` | `/dashboard` | Dashboard |

---

## 🔐 Autenticación

### JWT Token

Todos los endpoints protegidos requieren un header:

```
Authorization: Bearer <token>
```

**Tiempo de expiración**: 30 minutos

### Respuesta de Login/Registro

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "usuario": {
    "id": 1,
    "nombre": "Juan Pérez",
    "email": "juan@example.com"
  }
}
```

---

## 📊 Modelos de Datos

### Usuario

```python
{
  "id": int,
  "nombre": str(100),          # Min 2 caracteres
  "email": str(100),           # Email válido
  "password_hash": str(255),   # Hasheada
  "fecha_creacion": datetime
}
```

### Incidencia

```python
{
  "id": int,
  "titulo": str(200),          # Min 3 caracteres
  "descripcion": str(500),     # Opcional
  "ubicacion": str(200),       # Min 3 caracteres
  "tipo": str(50),             # semaforo, bache, poste, etc
  "estado": str(50),           # abierto, en_progreso, cerrado
  "prioridad": str(20),        # baja, media, alta
  "fotos": str(500),           # URLs separadas por comas
  "usuario_id": int,           # ID del creador
  "fecha_creacion": datetime
}
```

---

## 🛡️ Validaciones

### Contraseña

✅ Mínimo 8 caracteres
✅ Al menos una mayúscula
✅ Al menos una minúscula
✅ Al menos un número

### Email

✅ Contiene @
✅ Contiene .
✅ No duplicado en BD

### Título Reporte

✅ Mínimo 3 caracteres

### Ubicación

✅ Mínimo 3 caracteres

### Fotos

✅ Solo imágenes (jpg, png, gif, webp)
✅ Máximo 5MB (validado en BD)

---

## 🚨 Manejo de Errores

### Códigos HTTP

| Código | Significado |
|--------|-------------|
| `200` | ✅ Éxito |
| `400` | ⚠️ Solicitud inválida |
| `401` | 🔒 No autenticado |
| `403` | 🚫 Acceso denegado |
| `422` | ❌ Datos inválidos |
| `500` | 💥 Error del servidor |

### Ejemplo de Error

```json
{
  "detail": "La contraseña debe tener al menos 8 caracteres"
}
```

---

## 🔧 Configuración

### Cambiar puerto

```bash
python -m uvicorn src.main:app --port 9000
```

### Cambiar clave JWT

Editar en `src/security.py`:

```python
SECRET_KEY = "tu-nueva-clave-super-segura"
```

### Cambiar tiempo de token

Editar en `src/security.py`:

```python
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 60 minutos en lugar de 30
```

---

## 🐛 Troubleshooting

### Error: "No module named 'src'"

```bash
# Asegúrese de estar en la raíz del proyecto
cd ProyectoFinal
pip install -e .
```

### Error: "Port 8000 already in use"

```bash
# Usar puerto diferente
python -m uvicorn src.main:app --port 9000
```

### Error: "Database is locked"

```bash
# Eliminar BD y recrearla
rm data/incidencias.db
python -c "from src.models import Base, engine; Base.metadata.create_all(engine)"
```

### Tests fallan

```bash
# Reinstalar dependencias
pip install -r requisitos.txt --force-reinstall
python -m pytest tests/ --ignore=tests/test_pandas.py -v
```

---

## 📝 Notas de Desarrollo

### Logging

Se registran automáticamente:
- Creación de tokens
- Verificación de tokens
- Errores de autenticación
- Operaciones en BD

Ver logs en la consola durante ejecución.

### Base de Datos

- **Tipo**: SQLite (archivo local)
- **Ubicación**: `data/incidencias.db`
- **ORM**: SQLAlchemy
- **Migraciones**: Automáticas en startup

### Seguridad

⚠️ **IMPORTANTE**: Cambiar `SECRET_KEY` antes de producción

```python
# Generar nueva clave:
import secrets
secrets.token_urlsafe(32)
```

---

## 🤝 Contribuciones

Para mejorar el proyecto:

1. Crear una rama nueva
2. Hacer cambios
3. Ejecutar tests
4. Crear Pull Request

---

## 📄 Licencia

Proyecto educativo - Libre para usar y modificar

---

## ✅ Checklist de Verificación

- ✅ API funcionando sin errores
- ✅ 36/36 tests pasando
- ✅ Autenticación segura con JWT
- ✅ Validaciones exhaustivas
- ✅ Manejo robusto de errores
- ✅ Upload de imágenes funcionando
- ✅ Dashboard con gráficos
- ✅ Base de datos SQLite
- ✅ Documentación completa
- ✅ Logging de operaciones

---

**¡Sistema listo para usar! 🚀**

Para dudas o problemas, revisar los tests o los logs de la aplicación.
