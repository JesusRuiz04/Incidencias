# 🚀 Guía de Instalación y Configuración

## Índice
1. [⚡ Inicio Rápido (5 minutos)](#-inicio-rápido-5-minutos)
2. [Requisitos Previos](#requisitos-previos)
3. [Instalación Windows](#instalación-windows)
4. [Instalación Mac/Linux](#instalación-maclinux)
5. [Verificación](#verificación)
6. [Ejecución](#ejecución)
7. [Características Principales](#características-principales)
8. [Ejecución de Tests](#ejecución-de-tests)
9. [Solución de Problemas](#-solución-de-problemas)

---
9
## ⚡ Inicio Rápido (5 minutos)

**Si ya tienes Python y Git instalados, sigue estos pasos:**

### 1️⃣ Crear Carpeta de Datos

```bash
# Windows (PowerShell)
mkdir data

# Mac/Linux
mkdir -p data
```

### 2️⃣ Instalar Dependencias

```bash
pip install -r requisitos.txt
```

### 3️⃣ Crear Base de Datos

```bash
python seed_db.py
```

Esto crea 2 usuarios y 8 reportes de ejemplo.

### 4️⃣ Ejecutar Servidor

```bash
cd Incidencias
python -m uvicorn src.main:app --host 127.0.0.1 --port 8001
```

Deberías ver:
```
INFO:     Uvicorn running on http://127.0.0.1:8001
```

### 5️⃣ Abrir en Navegador

```
http://localhost:8001
```

### 6️⃣ Iniciar Sesión

| Email | Contraseña |
|-------|-----------|
| juan@example.com | Password123 |
| maria@example.com | Password456 |

---

---

## ✅ Requisitos Previos

- **Python 3.10 o superior** (ver `requisitos.txt` para versiones soportadas)
- **Git** (opcional, para clonar el repositorio)
- **Terminal/PowerShell**
- Espacio en disco: ~500 MB

### Verificar Python

```bash
python --version
# o
python3 --version
```

Debería mostrar Python 3.10 o superior.

---

## 🪟 Instalación Windows

### Paso 0: Preparar la Carpeta (IMPORTANTE)

Asegúrate de que existe la carpeta `data/`:

```powershell
# Si no existe, créala
mkdir data
```

**Nota**: Esta carpeta es necesaria para que la base de datos SQLite se cree correctamente.

### Paso 1: Descargar el Proyecto

```bash
# Opción A: Con Git
git clone <url-del-repositorio>
cd ProyectoFinal

# Opción B: Descargar ZIP
# - Descargar ZIP del repositorio
# - Extraer en una carpeta
# - Abrir PowerShell en esa carpeta
```

### Paso 2: Crear Entorno Virtual

```powershell
python -m venv .venv
```

### Paso 3: Activar Entorno Virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

**Nota**: Si tienes error de ejecución, ejecuta primero:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Deberías ver `(.venv)` al inicio de la línea de comando.

### Paso 4: Instalar Dependencias

```bash
pip install -r requisitos.txt
```

Espera a que complete la instalación (puede tomar 2-3 minutos).

### Paso 5: Crear Base de Datos (Opcional)

```bash
python seed_db.py
```

Esto crea:
- 2 usuarios de prueba
- 8 reportes de ejemplo
- Imágenes para los reportes

### Paso 6: Ejecutar Servidor

```bash
cd Incidencias
python -m uvicorn src.main:app --host 127.0.0.1 --port 8001
```

Deberías ver:
```
INFO:     Uvicorn running on http://127.0.0.1:8001
```

---

## 🍎 Instalación Mac/Linux

### Paso 0: Preparar la Carpeta (IMPORTANTE)

Asegúrate de que existe la carpeta `data/`:

```bash
# Si no existe, créala
mkdir -p data
```

**Nota**: Esta carpeta es necesaria para que la base de datos SQLite se cree correctamente.

### Paso 1: Descargar el Proyecto

```bash
# Con Git
git clone <url-del-repositorio>
cd ProyectoFinal

# O descargar ZIP manualmente
```

### Paso 2: Crear Entorno Virtual

```bash
python3 -m venv .venv
```

### Paso 3: Activar Entorno Virtual

```bash
source .venv/bin/activate
```

Deberías ver `(.venv)` al inicio de la línea.

### Paso 4: Instalar Dependencias

```bash
pip install -r requisitos.txt
```

### Paso 5: Crear Base de Datos (Opcional)

```bash
python seed_db.py
```

### Paso 6: Ejecutar Servidor

```bash
cd Incidencias
python -m uvicorn src.main:app --host 127.0.0.1 --port 8001
```

Accede a: **http://localhost:8001**

---

## ✔️ Verificación

### Verificar Instalación Correcta

```bash
# 1. Verificar que estés en el entorno virtual
# Deberías ver (.venv) en tu terminal

# 2. Verificar que las dependencias están instaladas
pip list | grep -E "fastapi|pandas|sqlalchemy"

# 3. Ejecutar los tests
python -m pytest tests/ -v
```

Deberías ver: `54 passed in X.XXs`

---

## ▶️ Ejecución

### Opción 1: Modo Desarrollo (Recomendado)

```bash
cd Incidencias
python -m uvicorn src.main:app --host 127.0.0.1 --port 8001
```

**Ventajas:**
- Mejor para debugging
- Mensajes de error detallados
- Puerto dedicado para desarrollo

### Opción 2: Modo Producción

```bash
cd Incidencias
python -m uvicorn src.main:app --host 0.0.0.0 --port 8001 --workers 4
```

**Ventajas:**
- Mejor rendimiento
- Múltiples workers

### Opción 3: Usar Puerto Diferente

```bash
cd Incidencias
python -m uvicorn src.main:app --host 127.0.0.1 --port 9000
```

Luego accede a `http://localhost:9000`

---

## 🌐 Acceder a la Aplicación

Una vez ejecutado el servidor:

1. Abre tu navegador
2. Ve a: **http://localhost:8001**
3. Deberías ver la página de inicio

### URLs Principales

| Página | URL |
|--------|-----|
| Inicio | http://localhost:8001 |
| Login | http://localhost:8001/login.html |
| Dashboard | http://localhost:8001/dashboard |
| Crear Reporte | http://localhost:8001/reporte |
| Análisis | http://localhost:8001/analisis |
| Documentación API | http://localhost:8001/docs |

### Documentación de API (Swagger)

Accede a: **http://localhost:8001/docs**

Aquí puedes:
- Ver todos los endpoints
- Probar endpoints directamente
- Ver esquemas de request/response

---

## 🎯 Características Principales

### Dashboard
- `http://localhost:8001/dashboard` - Ver estadísticas y reportes

### Crear Reporte
- `http://localhost:8001/reporte` - Crear nuevo reporte

### Análisis Avanzado (NUEVO)
- `http://localhost:8001/analisis` - Análisis con pandas

### API Docs
- `http://localhost:8001/docs` - Probar endpoints

---

## 🧪 Ejecución de Tests

### Todos los Tests

```bash
python -m pytest tests/ -v
```

Deberías ver: `54 passed`

### Tests Específicos

```bash
# Solo API
python -m pytest tests/test_api.py -v

# Solo autenticación
python -m pytest tests/test_auth_service.py -v

# Solo pandas
python -m pytest tests/test_pandas_analytics.py -v

# Con cobertura
python -m pytest tests/ --cov=src --cov-report=html
```

### Reporte de Cobertura

Después de ejecutar con `--cov`:

```bash
# Ver reporte HTML
# Abre: htmlcov/index.html en tu navegador
```

---

## 📊 Preparar Datos de Prueba

### Opción 1: Script Automático

```bash
python seed_db.py
```

Crea automáticamente:
- 2 usuarios
- 8 reportes
- Imágenes de ejemplo

**Credenciales:**
- Email: `juan@example.com`
- Contraseña: `Password123`

### Opción 2: Crear Manualmente

1. Abre http://localhost:8001/login.html
2. Haz clic en "Registrarse"
3. Llena el formulario:
   - Nombre: Tu nombre
   - Email: tu@email.com
   - Contraseña: MinPassword123 (8+ caracteres, mayúscula, minúscula, número)
4. Haz clic en "Crear Cuenta"

---

## 🔐 Credenciales de Prueba

Después de ejecutar `seed_db.py`:

| Email | Contraseña | Nombre |
|-------|-----------|--------|
| juan@example.com | Password123 | Juan Pérez |
| maria@example.com | Password456 | María García |

---

## 🛑 Detener el Servidor

Presiona `Ctrl+C` en la terminal donde está ejecutándose el servidor.

---

## 🔄 Actualizar Dependencias

```bash
# Actualizar todas
pip install --upgrade -r requisitos.txt

# Actualizar una específica
pip install --upgrade pandas
```

---

## 🗑️ Limpiar la Instalación

### Eliminar Entorno Virtual

```bash
# Windows
rmdir /s /q .venv

# Mac/Linux
rm -rf .venv
```

### Eliminar Base de Datos

```bash
# Windows
del data\incidencias.db

# Mac/Linux
rm data/incidencias.db
```

### Eliminar Caché de Python

```bash
# Windows
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"

# Mac/Linux
find . -type d -name __pycache__ -exec rm -r {} +
```

---

## 🐛 Solución de Problemas

### 🔧 Problemas de Compatibilidad Python 3.13

Si tienes errores durante la instalación con Python 3.13, revisa `requisitos.txt` - las versiones están optimizadas para máxima compatibilidad.

#### Problema: Error con Pillow durante la instalación

**Error:**
```
KeyError: '__version__'
```

**Solución:**
```bash
# Instalar sin aislamiento de construcción
pip install pillow --no-build-isolation

# O actualizar
pip install pillow --upgrade
```

#### Problema: Error con SQLAlchemy en Python 3.13

**Error:**
```
AssertionError: Class directly inherits TypingOnly but has additional attributes
```

**Solución:**
```bash
# Actualizar SQLAlchemy
pip install --upgrade sqlalchemy
```

Si los problemas persisten, revisa `requisitos.txt` para las versiones pinned recomendadas.

### Problema 1: Python no encontrado

**Error:**
```
python: command not found
```

**Solución:**
- Asegúrate de tener Python instalado
- En Windows, usa `python` en lugar de `python3`
- En Mac/Linux, usa `python3` en lugar de `python`

### Problema 2: No puedo activar el entorno virtual

**Error:**
```
cannot be loaded because running scripts is disabled
```

**Solución Windows:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1
```

### Problema 3: Las dependencias no se instalan

**Error:**
```
ERROR: Could not find a version that satisfies
```

**Solución:**
```bash
# Actualizar pip
python -m pip install --upgrade pip

# Reinstalar requisitos
pip install -r requisitos.txt --force-reinstall

# Si sigue fallando, instalar sin cache
pip install --no-cache-dir -r requisitos.txt
```

### Problema 4: Puerto 8001 ya está en uso

**Error:**
```
Address already in use
```

**Solución:**
```bash
# Opción A: Usar puerto diferente
cd Incidencias
python -m uvicorn src.main:app --host 127.0.0.1 --port 9000

# Opción B: Matar proceso en puerto 8001 (Windows)
netstat -ano | findstr :8001
taskkill /PID <PID> /F

# Opción C: Matar proceso en puerto 8001 (Mac/Linux)
lsof -i :8001
kill -9 <PID>
```

### Problema 5: "No module named pandas"

**Error:**
```
ModuleNotFoundError: No module named 'pandas'
```

**Solución:**
```bash
# Asegúrate de tener activado el entorno virtual
# Luego instala
pip install pandas
```

### Problema 6: "Database not found" o "unable to open database file"

**Error:**
```
sqlite3.OperationalError: unable to open database file
```

**Causa:** La carpeta `data/` no existe

**Solución:**
```bash
# Crear la carpeta
mkdir data

# Luego ejecutar
python seed_db.py
```
mkdir data

# Luego ejecutar seed_db.py
python seed_db.py
```

### Problema 8: Los tests fallan

**Solución:**
```bash
# Verificar instalación
pip install -r requisitos.txt --force-reinstall

# Limpiar caché
pip cache purge

# Ejecutar tests nuevamente
python -m pytest tests/ -v
```

### Problema 9: Las imágenes no se cargan

**Solución:**
```bash
# Crear carpeta uploads
mkdir static/uploads

# Verificar permisos
# (Windows no requiere, Mac/Linux: chmod 755 static/uploads)
```

### Problema 10: Pandas no se instala

**Solución:**
```bash
# Instalar versión compatible
pip install pandas==3.0.2

# O instalar dependencias
pip install numpy pandas
```

---

## 📝 Notas Importantes

1. **Siempre activar el entorno virtual** antes de trabajar
2. **Cambiar SECRET_KEY** antes de ir a producción
3. **Usar variables de entorno** para datos sensibles
4. **Hacer backup de base de datos** regularmente
5. **Actualizar dependencias** periódicamente

---

## ✅ Checklist de Instalación

- [ ] Python 3.10+ instalado
- [ ] Proyecto descargado
- [ ] Entorno virtual creado
- [ ] Entorno virtual activado
- [ ] Dependencias instaladas
- [ ] Base de datos creada (seed_db.py)
- [ ] Servidor ejecutándose
- [ ] Acceso a http://localhost:8001
- [ ] Tests pasando (54/54)
- [ ] Credenciales funcionan

---

## 🆘 Obtener Ayuda

1. **Ver logs del servidor**: Están en la terminal
2. **Revisar documentación API**: http://localhost:8001/docs
3. **Ejecutar tests**: `python -m pytest tests/ -v`
4. **Limpiar caché**: `pip cache purge`

---

## 🎉 ¡Instalación Completada!

El sistema está funcionando. ¡Comienza a explorar!

**URLs principales:**
- Inicio: http://localhost:8001
- Login: http://localhost:8001/login.html
- Dashboard: http://localhost:8001/dashboard

Para más información consulta [README.md](README.md)

El sistema está listo para usar. Accede a:

- **Inicio**: http://localhost:8001
- **Login**: http://localhost:8001/login.html
- **API Docs**: http://localhost:8001/docs

**¡Disfruta el sistema!** 🚀
