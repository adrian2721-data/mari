from pathlib import Path
from typing import Annotated

from fastapi import File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_offline import FastAPIOffline
from routes import categoria,proveedor,producto,tienda
from bd import *
import logging
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


templates = Jinja2Templates(directory="templates")#directorio de los html
app = FastAPIOffline(
    title="Mi API de Productos",
    description="API para gestionar productos de una tienda",
    version="1.0.0",
    tags=["Bases de datos"]
)
app.mount("/static", StaticFiles(directory="static"), name="static")#cargar los css



@app.get("/test")
def raiz():
    return {"mensaje": "Bienvenido a la API de flores"}
@app.get("/check-db")
def check_db():
    """Endpoint para verificar el estado de la base de datos"""
    try:
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        return {
            "status": "success",
            "tables": tables,
            "database": DB_NAME
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

# Evento de inicio para crear tablas
@app.on_event("startup")
def on_startup():
    logger.info("🚀 Iniciando aplicación...")
    try:
        create_tables()
    except Exception as e:
        logger.error(f"❌ No se pudieron crear las tablas: {e}")

        
        
app.include_router(categoria.router)
app.include_router(proveedor.router)
app.include_router(producto.router)
app.include_router(tienda.router)

if __name__ == "__main__":
    import uvicorn

    # Crear tablas antes de iniciar
    logger.info("🔧 Creando tablas antes del inicio...")
    try:
        create_tables()
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}")
        exit(1)

    logger.info("🚀 Iniciando servidor...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    


