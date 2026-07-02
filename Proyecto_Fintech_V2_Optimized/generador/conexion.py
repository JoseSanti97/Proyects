from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Estructura de la URL de tu conexión: postgresql://usuario:contraseña@host:puerto/nombre_bd
DATABASE_URL = "postgresql://usuario:contraseña@host:puerto/nombre_bd" #usa tu contraseña y nombre de tu bd


engine = create_engine(
    DATABASE_URL, 
    echo=False,
    pool_size=10,         # Mantiene hasta 10 conexiones físicas abiertas en reserva
    max_overflow=20,      # Permite abrir hasta 20 conexiones extra bajo alta demanda de lotes
    pool_recycle=1800,     # Recicla las conexiones cada 30 minutos para evitar hilos huérfanos
    pool_pre_ping=True    # Verifica si la conexión con Docker sigue viva antes de enviar el lote
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def obtener_sesion():
    sesion = SessionLocal()
    try:
        return sesion
    except Exception as e:
        print(f"Error al crear la sesión de SQLAlchemy: {e}")
        sesion.close()
        return None