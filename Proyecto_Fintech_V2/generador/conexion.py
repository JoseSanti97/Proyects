from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Estructura de la URL de tu conexión: postgresql://usuario:contraseña@host:puerto/nombre_bd
DATABASE_URL = "postgresql://usuario:contraseña@host:puerto/nombre_bd"

# El Engine es el encargado de administrar las conexiones con Docker
engine = create_engine(DATABASE_URL, echo=False)

# SessionLocal fábrica las conexiones con los scripts
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def obtener_sesion():
    sesion = SessionLocal()
    try:
        return sesion
    except Exception as e:
        print(f"Error al crear la sesión de SQLAlchemy: {e}")
        sesion.close()
        return None