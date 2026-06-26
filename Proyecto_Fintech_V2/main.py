import sys
from generador.conexion import obtener_sesion
from generador.poblador_masivo import poblar_sistema
from generador.conexion import engine
from generador.modelos import Base

def ejecutar_pipeline_fintech():
    print("--- INICIANDO CORE BANCARIO FINTECH ---")

    print("Creando tablas en la base de datos si no existen")
    Base.metadata.create_all(bind=engine)

    session = obtener_sesion()
    
    if not session:
        print("Error: No se pudo establecer la sesión con el servidor PostgreSQL.")
        sys.exit(1)
        
    try:
        poblar_sistema(session, total_clientes=500, transacciones_por_cliente=5)
        
    except Exception as error:
        print(f"Error: {error}")
        
    finally:
        session.close()
        print("Conexión con el contenedor Docker cerrada de forma segura.")
        print("--- FIN DEL PROCESO ---")

if __name__ == "__main__":
    ejecutar_pipeline_fintech()