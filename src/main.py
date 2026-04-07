"""
API FastAPI para sistema de incidencias de tráfico.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(title="Sistema de Incidencias de Tráfico")

# Servir archivos estáticos (CSS, JS, imágenes)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """Sirve la página de inicio."""
    return FileResponse("templates/index.html")


@app.get("/index.html")
async def index():
    """Sirve la página de inicio."""
    return FileResponse("templates/index.html")


@app.get("/login.html")
async def login():
    """Sirve la página de login/registro."""
    return FileResponse("templates/login.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)





