import os

from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
import logging

from sqlmodel import SQLModel, Session, create_engine


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    filename="log.txt",
    filemode="a",  # de escritutra en el archivo
)

logger = logging.getLogger(__name__)

load_dotenv()

# Configuración desde variables de entorno
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")
# DB_NAME = os.getenv("DB_NAME")

# # Verificar que las variables existen
# if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
#     logger.error("❌ Faltan variables de entorno. Verifica tu archivo .env")
#     exit(1)

# logger.info(f"📊 Conectando a: {DB_HOST}:{DB_PORT}/{DB_NAME} con usuario {DB_USER}")

# URL de conexión para MySQL - usando pymysql para mejor compatibilidad
DATABASE_URL = f"sqlite:///fasttienda"
logger.info(f"🔗 URL de conexión: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL, echo=True)
    logger.info("✅ Engine creado correctamente")
except Exception as e:
    logger.error(f"❌ Error al crear engine: {e}")
    exit(1)


# Función para crear tablas con manejo de errores
def create_tables():
    try:
        logger.info("🔄 Intentando crear tablas...")

        # Verificar conexión primero
        with engine.connect() as conn:
            logger.info("✅ Conexión a la base de datos exitosa")

        # Crear todas las tablas
        SQLModel.metadata.create_all(engine)
        logger.info("✅ Tablas creadas exitosamente")

        # Verificar que las tablas se crearon
        from sqlalchemy import inspect

        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"📋 Tablas existentes: {tables}")

    except SQLAlchemyError as e:
        logger.error(f"❌ Error de SQLAlchemy al crear tablas: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Error inesperado al crear tablas: {e}")
        raise

def get_session():
    with Session(engine) as session:
        yield session