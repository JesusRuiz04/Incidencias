"""
API FastAPI para sistema de incidencias de tráfico.
Incluye: autenticación JWT, creación/listado de reportes, dashboard, upload de fotos.
"""

from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, Form, status, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
from pydantic import BaseModel
from .models import Incidencia, Usuario, SessionLocal
from .security import create_access_token, verify_token, hash_password, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from .auth_service import validar_email, validar_fuerza_password
from jose import jwt, JWTError
from .analytics_pandas import obtener_reportes_por_periodo, obtener_tendencias, exportar_reportes_csv
from datetime import timedelta
from pathlib import Path

app = FastAPI(title="Sistema de Incidencias de Tráfico")

# Configurar Jinja2Templates con ruta absoluta
BASE_DIR = Path(__file__).parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Desabilitar cache de Jinja2 para evitar errores de tipos unhashable
templates.env.cache = None

# Helper function para renderizar templates
def render_template(template_name: str, context: dict) -> HTMLResponse:
    """Renderiza un template Jinja2 y retorna una HTMLResponse."""
    template = templates.get_template(template_name)
    html_content = template.render(context)
    return HTMLResponse(content=html_content)

# ==================== FUNCIONES DE AUTENTICACIÓN ====================

def obtener_usuario_desde_cookie(request: Request):
    """Obtiene el usuario logeado desde la cookie del token."""
    token = request.cookies.get("access_token")
    if not token:
        return None
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id: str = payload.get("sub")
        if usuario_id is None:
            return None
        
        db = SessionLocal()
        usuario = db.query(Usuario).filter(Usuario.id == int(usuario_id)).first()
        db.close()
        return usuario
    except JWTError:
        return None


# Modelos Pydantic
class IncidenciaCreate(BaseModel):
    titulo: str
    descripcion: str = None
    ubicacion: str
    tipo: str
    prioridad: str = "media"
    fotos: str = None
    estado: str = "abierto"

class UsuarioRegistro(BaseModel):
    nombre: str
    email: str
    password: str

class UsuarioLogin(BaseModel):
    email: str
    password: str

# Crear carpeta de uploads
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Servir archivos estáticos (CSS, JS, imágenes)
STATIC_DIR = BASE_DIR / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ==================== RUTAS DE PÁGINAS ====================

@app.get("/")
async def root(request: Request):
    """Sirve la página de inicio."""
    usuario = obtener_usuario_desde_cookie(request)
    return render_template("index.html", {"request": request, "usuario": usuario})



@app.get("/login")
async def login_page(request: Request):
    """Sirve la página de login/registro."""
    usuario = obtener_usuario_desde_cookie(request)
    return render_template("login.html", {"request": request, "usuario": usuario})


@app.get("/login.html")
async def login_html(request: Request):
    """Sirve la página de login/registro."""
    usuario = obtener_usuario_desde_cookie(request)
    return render_template("login.html", {"request": request, "usuario": usuario})


@app.post("/login")
async def login_form(request: Request, email: str = Form(...), password: str = Form(...)):
    """Procesa login desde formulario HTML."""
    from fastapi.responses import RedirectResponse
    db = SessionLocal()
    try:
        # Buscar usuario
        usuario_db = db.query(Usuario).filter(Usuario.email == email).first()
        
        if not usuario_db or not verify_password(password, usuario_db.password_hash):
            # Regresar al login con error
            return render_template("login.html", {
                "request": request,
                "error_message": "Email o contraseña incorrectos"
            })
        
        # Crear token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(usuario_db.id)},
            expires_delta=access_token_expires
        )
        
        # Redirigir al dashboard y guardar token en cookie
        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return response
    
    except Exception as e:
        return render_template("login.html", {
            "request": request,
            "error_message": f"Error al iniciar sesión: {str(e)}"
        })
    finally:
        db.close()


@app.post("/register")
async def register_form(request: Request, username: str = Form(...), email: str = Form(...), 
                       password: str = Form(...), password_confirm: str = Form(...)):
    """Procesa registro desde formulario HTML."""
    from fastapi.responses import RedirectResponse
    db = SessionLocal()
    try:
        # Validaciones
        if password != password_confirm:
            return render_template("login.html", {
                "request": request,
                "error_message": "Las contraseñas no coinciden"
            })
        
        if len(username.strip()) < 2:
            return render_template("login.html", {
                "request": request,
                "error_message": "El nombre de usuario debe tener al menos 2 caracteres"
            })
        
        if not validar_email(email):
            return render_template("login.html", {
                "request": request,
                "error_message": "Email inválido"
            })
        
        if not validar_fuerza_password(password):
            return render_template("login.html", {
                "request": request,
                "error_message": "La contraseña debe tener al menos 8 caracteres, mayúscula, minúscula y número"
            })
        
        # Verificar si el email ya existe
        usuario_existente = db.query(Usuario).filter(Usuario.email == email).first()
        if usuario_existente:
            return render_template("login.html", {
                "request": request,
                "error_message": "El email ya está registrado"
            })
        
        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            nombre=username,
            email=email,
            password_hash=hash_password(password)
        )
        
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        
        # Crear token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(nuevo_usuario.id)},
            expires_delta=access_token_expires
        )
        
        # Redirigir al dashboard y guardar token en cookie
        response = RedirectResponse(url="/dashboard", status_code=303)
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return response
    
    except Exception as e:
        db.rollback()
        return render_template("login.html", {
            "request": request,
            "error_message": f"Error al registrarse: {str(e)}"
        })
    finally:
        db.close()


@app.get("/logout")
async def logout(request: Request):
    """Cierra la sesión del usuario."""
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="access_token")
    return response


@app.post("/crear_reporte")
async def crear_reporte_form(
    request: Request,
    tipo_incidencia: str = Form(...),
    severidad: str = Form(...),
    ubicacion: str = Form(...),
    descripcion: str = Form(...),
    fecha: str = Form(...),
    hora: str = Form(None),
    fotos: List[UploadFile] = File([]),
    contacto: str = Form(None)
):
    """Procesa creación de reporte desde formulario HTML."""
    db = SessionLocal()
    try:
        # Obtener usuario del token de la cookie
        token = request.cookies.get("access_token")
        usuario_id = 1  # ID por defecto para testing
        
        if token:
            try:
                token_data = verify_token(token)
                usuario_id = token_data.get("usuario_id", 1)
            except:
                pass
        
        # Validar campos obligatorios
        if not ubicacion or len(ubicacion.strip()) < 3:
            return render_template("reporte.html", {
                "request": request,
                "error_message": "La ubicación debe tener al menos 3 caracteres"
            })
        
        if not descripcion or len(descripcion.strip()) < 5:
            return render_template("reporte.html", {
                "request": request,
                "error_message": "La descripción debe tener al menos 5 caracteres"
            })
        
        # Procesar fotos subidas
        fotos_urls = []
        if fotos and len(fotos) > 0:
            import time
            for file in fotos:
                # Saltar archivos sin nombre o que no sean válidos
                if not file or not file.filename or file.size == 0:
                    continue
                
                # Validar que sea una imagen
                if not file.content_type or not file.content_type.startswith('image/'):
                    continue
                
                try:
                    # Generar nombre único con timestamp
                    timestamp = int(time.time() * 1000)
                    # Limpiar el nombre del archivo
                    safe_filename = "".join(c for c in file.filename if c.isalnum() or c in ('-', '_', '.'))
                    filename = f"reporte_{usuario_id}_{timestamp}_{safe_filename}"
                    filepath = UPLOAD_DIR / filename
                    
                    # Guardar archivo
                    contents = await file.read()
                    if contents:  # Solo guardar si hay contenido
                        with open(filepath, "wb") as f:
                            f.write(contents)
                        fotos_urls.append(f"/static/uploads/{filename}")
                except Exception as e:
                    print(f"Error subiendo foto: {str(e)}")
        
        # Crear la incidencia
        nueva_incidencia = Incidencia(
            titulo=f"Reporte: {tipo_incidencia}",
            descripcion=descripcion,
            ubicacion=ubicacion,
            tipo=tipo_incidencia,
            prioridad=severidad,
            fotos=",".join(fotos_urls) if fotos_urls else None,
            estado="abierto",
            usuario_id=usuario_id
        )
        
        db.add(nueva_incidencia)
        db.commit()
        db.refresh(nueva_incidencia)
        
        # Redirigir al dashboard
        response = RedirectResponse(url="/dashboard", status_code=303)
        return response
    
    except Exception as e:
        db.rollback()
        print(f"Error creando reporte: {str(e)}")
        import traceback
        traceback.print_exc()
        return render_template("reporte.html", {
            "request": request,
            "error_message": f"Error al crear reporte: {str(e)}"
        })
    finally:
        db.close()


@app.get("/reporte")
async def reporte_page(request: Request):
    """Sirve la página para crear reportes (protegida)."""
    usuario = obtener_usuario_desde_cookie(request)
    if not usuario:
        return RedirectResponse(url="/login", status_code=303)
    
    return render_template("reporte.html", {
        "request": request,
        "usuario": usuario
    })


@app.post("/cerrar_reporte/{reporte_id}")
async def cerrar_reporte(request: Request, reporte_id: int):
    """Cierra un reporte (solo para admins)."""
    usuario = obtener_usuario_desde_cookie(request)
    
    # Verificar si está logeado y es admin
    if not usuario or not usuario.es_admin:
        return RedirectResponse(url="/login", status_code=303)
    
    db = SessionLocal()
    try:
        # Obtener el reporte
        reporte = db.query(Incidencia).filter(Incidencia.id == reporte_id).first()
        
        if not reporte:
            return RedirectResponse(url="/dashboard", status_code=303)
        
        # Cerrar el reporte
        reporte.estado = "cerrado"
        db.commit()
        
        return RedirectResponse(url="/dashboard", status_code=303)
    
    except Exception as e:
        db.rollback()
        print(f"Error cerrando reporte: {str(e)}")
        return RedirectResponse(url="/dashboard", status_code=303)
    finally:
        db.close()


@app.get("/dashboard")
async def dashboard_page(request: Request):
    """Sirve el dashboard de estadísticas (protegido)."""
    # Verificar si el usuario está logeado
    usuario = obtener_usuario_desde_cookie(request)
    if not usuario:
        return RedirectResponse(url="/login", status_code=303)
    
    db = SessionLocal()
    try:
        # Todos los usuarios ven todos los reportes (admins y no-admins)
        incidencias = db.query(Incidencia).all()
        es_admin = usuario.es_admin
        
        # Calcular estadísticas
        total_incidents = len(incidencias)
        pending_incidents = len([i for i in incidencias if i.estado == "en_progreso"])
        resolved_incidents = len([i for i in incidencias if i.estado == "cerrado"])
        
        # Contar incidencias del mes actual
        from datetime import datetime
        current_month = datetime.now().month
        current_year = datetime.now().year
        monthly_incidents = len([
            i for i in incidencias 
            if i.fecha_creacion.month == current_month and i.fecha_creacion.year == current_year
        ])
        
        # Calcular datos por tipo de incidencia
        from collections import Counter
        tipos_counter = Counter([inc.tipo for inc in incidencias if inc.tipo])
        chart_data = {
            "labels": list(tipos_counter.keys()),
            "data": list(tipos_counter.values())
        }
        
        # Calcular datos por mes (últimos 12 meses)
        from datetime import timedelta, datetime
        meses_data = {}
        hoy = datetime.now()
        
        for i in range(11, -1, -1):  # Últimos 12 meses
            fecha = hoy - timedelta(days=30*i)
            mes_key = fecha.strftime("%m/%Y")
            meses_data[mes_key] = 0
        
        for inc in incidencias:
            mes_key = inc.fecha_creacion.strftime("%m/%Y")
            if mes_key in meses_data:
                meses_data[mes_key] += 1
        
        trend_data = {
            "labels": list(meses_data.keys()),
            "data": list(meses_data.values())
        }
        
        # Obtener reportes recientes
        recent_reports = []
        for inc in sorted(incidencias, key=lambda x: x.fecha_creacion, reverse=True)[:5]:
            # Procesar estado para mostrar
            status_map = {
                "abierto": "abierto",
                "en_progreso": "en_progreso",
                "cerrado": "cerrado"
            }
            status_label_map = {
                "abierto": "Abierto",
                "en_progreso": "En Progreso",
                "cerrado": "Cerrado"
            }
            
            # Procesar imágenes
            images = []
            if inc.fotos:
                images = [img.strip() for img in inc.fotos.split(",") if img.strip()]
            
            # Obtener nombre del usuario que creó el reporte
            usuario_creador = db.query(Usuario).filter(Usuario.id == inc.usuario_id).first()
            reporter_name = usuario_creador.nombre if usuario_creador else "Desconocido"
            
            recent_reports.append({
                "id": inc.id,
                "title": inc.titulo,
                "location": inc.ubicacion,
                "date": inc.fecha_creacion.strftime("%d/%m/%Y"),
                "reporter": reporter_name if es_admin else "Yo",
                "status": status_map.get(inc.estado, "abierto"),
                "status_label": status_label_map.get(inc.estado, "Abierto"),
                "images": images,
                "descripcion": inc.descripcion,
                "tipo": inc.tipo
            })
        
        return render_template("dashboard.html", {
            "request": request,
            "usuario": usuario,
            "es_admin": es_admin,
            "total_incidents": total_incidents,
            "pending_incidents": pending_incidents,
            "resolved_incidents": resolved_incidents,
            "monthly_incidents": monthly_incidents,
            "recent_reports": recent_reports,
            "has_chart_data": total_incidents > 0,
            "has_trend_data": total_incidents > 0,
            "chart_data": chart_data,
            "trend_data": trend_data
        })
    
    except Exception as e:
        print(f"Error en dashboard: {str(e)}")
        import traceback
        traceback.print_exc()
        return render_template("dashboard.html", {
            "request": request,
            "usuario": usuario,
            "es_admin": usuario.es_admin,
            "total_incidents": 0,
            "pending_incidents": 0,
            "resolved_incidents": 0,
            "monthly_incidents": 0,
            "recent_reports": [],
            "has_chart_data": False,
            "has_trend_data": False,
            "chart_data": {"labels": [], "data": []},
            "trend_data": {"labels": [], "data": []}
        })
    finally:
        db.close()


@app.get("/analisis")
async def analisis_page(request: Request):
    """Sirve la página de análisis avanzado con pandas."""
    # Verificar si el usuario está logeado
    usuario = obtener_usuario_desde_cookie(request)
    if not usuario:
        return RedirectResponse(url="/login", status_code=303)
    
    db = SessionLocal()
    try:
        # Todos los usuarios ven análisis de todos los reportes
        todos_reportes = db.query(Incidencia).all()
        
        # Calcular estadísticas básicas
        total_incidents = len(todos_reportes)
        abiertos = len([r for r in todos_reportes if r.estado == 'abierto'])
        en_progreso = len([r for r in todos_reportes if r.estado == 'en_progreso'])
        cerrados = len([r for r in todos_reportes if r.estado == 'cerrado'])
        
        # Obtener análisis con pandas
        analisis_periodo = obtener_reportes_por_periodo(usuario.id, "mensual")
        analisis_tendencias = obtener_tendencias(usuario.id, 30)
        
        # Preparar datos para gráficos
        # Gráfico por tipo
        tipos_count = {}
        for r in todos_reportes:
            tipos_count[r.tipo] = tipos_count.get(r.tipo, 0) + 1
        
        # Gráfico por prioridad
        prioridad_count = {}
        for r in todos_reportes:
            prioridad_count[r.prioridad] = prioridad_count.get(r.prioridad, 0) + 1
        
        # Prepare chart data
        chart_data = {
            "labels": list(tipos_count.keys()),
            "data": list(tipos_count.values())
        }
        
        return render_template("analisis.html", {
            "request": request,
            "usuario": usuario,
            "es_admin": usuario.es_admin,
            "total_incidents": total_incidents,
            "abiertos": abiertos,
            "en_progreso": en_progreso,
            "cerrados": cerrados,
            "tipos": list(tipos_count.keys()),
            "tipos_count": list(tipos_count.values()),
            "prioridades": list(prioridad_count.keys()),
            "prioridades_count": list(prioridad_count.values()),
            "analisis_periodo": analisis_periodo,
            "analisis_tendencias": analisis_tendencias,
            "chart_data": chart_data
        })
    finally:
        db.close()


# ==================== AUTENTICACIÓN ====================

@app.post("/api/auth/registro")
async def registro(usuario: UsuarioRegistro):
    """Registrar un nuevo usuario."""
    db = SessionLocal()
    try:
        # Validaciones
        if len(usuario.nombre.strip()) < 2:
            raise HTTPException(status_code=400, detail="El nombre debe tener al menos 2 caracteres")
        
        if not validar_email(usuario.email):
            raise HTTPException(status_code=400, detail="Email inválido")
        
        if not validar_fuerza_password(usuario.password):
            raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 8 caracteres, mayúscula, minúscula y número")
        
        # Verificar si el email ya existe
        usuario_existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
        if usuario_existente:
            raise HTTPException(status_code=400, detail="El email ya está registrado")
        
        # Crear nuevo usuario
        nuevo_usuario = Usuario(
            nombre=usuario.nombre,
            email=usuario.email,
            password_hash=hash_password(usuario.password)
        )
        
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        
        # Crear token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(nuevo_usuario.id)},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "usuario": {"id": nuevo_usuario.id, "nombre": nuevo_usuario.nombre, "email": nuevo_usuario.email}
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@app.post("/api/auth/login")
async def login(usuario: UsuarioLogin):
    """Iniciar sesión."""
    db = SessionLocal()
    try:
        # Buscar usuario
        usuario_db = db.query(Usuario).filter(Usuario.email == usuario.email).first()
        
        if not usuario_db or not verify_password(usuario.password, usuario_db.password_hash):
            raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
        
        # Crear token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(usuario_db.id)},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "usuario": {"id": usuario_db.id, "nombre": usuario_db.nombre, "email": usuario_db.email}
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


# ==================== REPORTES ====================

@app.post("/api/crear-reporte")
async def crear_reporte(
    incidencia: IncidenciaCreate,
    token: dict = Depends(verify_token)
):
    """Crea una nueva incidencia/reporte (requiere autenticación)."""
    db = SessionLocal()
    try:
        # Validar campos obligatorios
        if not incidencia.titulo or len(incidencia.titulo.strip()) < 3:
            raise HTTPException(status_code=400, detail="El título debe tener al menos 3 caracteres")
        
        if not incidencia.ubicacion or len(incidencia.ubicacion.strip()) < 3:
            raise HTTPException(status_code=400, detail="La ubicación debe tener al menos 3 caracteres")
        
        # Crear la incidencia
        nueva_incidencia = Incidencia(
            titulo=incidencia.titulo,
            descripcion=incidencia.descripcion,
            ubicacion=incidencia.ubicacion,
            tipo=incidencia.tipo,
            prioridad=incidencia.prioridad,
            fotos=incidencia.fotos,
            estado=incidencia.estado,
            usuario_id=token["usuario_id"]
        )
        
        db.add(nueva_incidencia)
        db.commit()
        db.refresh(nueva_incidencia)
        
        return {
            "id": nueva_incidencia.id,
            "mensaje": "Reporte creado exitosamente",
            "titulo": nueva_incidencia.titulo
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        db.close()


# ==================== UPLOAD DE FOTOS ====================

@app.post("/api/upload-foto")
async def upload_foto(
    file: UploadFile = File(...),
    token: dict = Depends(verify_token)
):
    """Subir una foto para un reporte."""
    try:
        # Validar que sea imagen
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
        
        # Generar nombre único
        filename = f"reporte_{token['usuario_id']}_{file.filename}"
        filepath = UPLOAD_DIR / filename
        
        # Guardar archivo
        contents = await file.read()
        with open(filepath, "wb") as f:
            f.write(contents)
        
        return {
            "filename": filename,
            "url": f"/static/uploads/{filename}",
            "mensaje": "Foto subida exitosamente"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== DASHBOARD / ESTADÍSTICAS ====================

@app.get("/api/reportes-por-periodo")
async def obtener_periodo(periodo: str = "semanal", token: dict = Depends(verify_token)):
    """
    Obtiene análisis de reportes agrupados por período (semanal o mensual).
    Utiliza pandas para análisis avanzados.
    """
    if periodo not in ["semanal", "mensual"]:
        raise HTTPException(status_code=400, detail="Período debe ser 'semanal' o 'mensual'")
    
    try:
        resultado = obtener_reportes_por_periodo(token["usuario_id"], periodo)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tendencias")
async def obtener_stats_tendencias(dias: int = 30, token: dict = Depends(verify_token)):
    """
    Obtiene tendencias de reportes en los últimos N días.
    Incluye velocidad de resolución y análisis diario.
    """
    if dias < 1 or dias > 365:
        raise HTTPException(status_code=400, detail="Días debe estar entre 1 y 365")
    
    try:
        resultado = obtener_tendencias(token["usuario_id"], dias)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/exportar-reportes")
async def exportar_datos(request: Request, formato: str = "csv"):
    """
    Exporta todos los reportes del usuario.
    Soporta formatos: csv, json
    """
    usuario = obtener_usuario_desde_cookie(request)
    if not usuario:
        raise HTTPException(status_code=401, detail="No autenticado")
    
    if formato not in ["csv", "json"]:
        raise HTTPException(status_code=400, detail="Formato debe ser 'csv' o 'json'")
    
    try:
        df = exportar_reportes_csv(usuario.id)
        
        if df.empty:
            raise HTTPException(status_code=404, detail="No hay reportes para exportar")
        
        if formato == "csv":
            # Guardar como CSV temporal
            archivo_temp = f"/tmp/reportes_{usuario.id}.csv"
            df.to_csv(archivo_temp, index=False, encoding='utf-8-sig')
            return FileResponse(
                path=archivo_temp,
                filename=f"reportes_{usuario.id}.csv",
                media_type="text/csv"
            )
        else:  # json
            return df.to_dict(orient='records')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
