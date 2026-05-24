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
   cd Incidencias
   python -m uvicorn src.main:app --host 127.0.0.1 --port 8001
   ```
   Accede a http://localhost:8001

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
│   ├── main.py                 # API FastAPI (18 endpoints)
│   ├── models.py               # Modelos SQLAlchemy
│   ├── security.py             # Autenticación y hashing
│   ├── config.py               # Configuración
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
|--------|----------|-------------|(API) |
| POST | `/crear_reporte` | Crear reporte (web) |
| GET | `/reporte` | Página de crear reporte |
| POST | `/cerrar_reporte/{id}` | Cerrar reporte |
| POST | `/api/upload-foto` | Subir foto para reporte |

### Páginas Web
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Página de inicio |
| GET | `/login` | Redirigir a login |
| GET | `/login.html` | Formulario login/registro |
| GET | `/logout` | Cerrar sesión |
| GET | `/dashboard` | Dashboard con estadísticas |
| GET | `/analisis` | Análisis avanzado con pandas |

### ⭐ Análisis Avanzado (Pandas)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/reportes-por-periodo` | Análisis semanal/mensual |
| GET | `/api/tendencias` | Tendencias de últimos 30 días |
| GET | `/api/exportar-reportes` | Descargar reportes (CSV/JSON
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

Acceda a: **http://localhost:8001/analisis**

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
| Última actualización | Mayo 2026 |
| Tests | 54/54 ✅ |
| Endpoints | 18 |
| Cobertura | Completa |
| Estado | Production Ready |


