import psycopg2
from generador.conexion import obtener_conexion
from generador.poblador_masivo import poblar_sistema_fintech

def ejecutar_archivo_sql(conexion, ruta_archivo):
    """Abre el archivo SQL"""
    cursor = conexion.cursor()
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        cursor.execute(f.read())
    conexion.commit()
    cursor.close()
    print(f"✅ Completado: {ruta_archivo}")

if __name__ == "__main__":
    print("Desplegando Base de Datos")
    
    try:
        # 1. Abrimos conexión global
        conn = obtener_conexion()
        
        # 2. Corremos los scripts_sql en orden secuencial
        ejecutar_archivo_sql(conn, "scripts_sql/01_schema.sql")
        ejecutar_archivo_sql(conn, "scripts_sql/02_constraints.sql")
        ejecutar_archivo_sql(conn, "scripts_sql/03_triggers.sql")
        ejecutar_archivo_sql(conn, "scripts_sql/04_procedures.sql")
        ejecutar_archivo_sql(conn, "scripts_sql/06_escenarios.sql")
        
        # Cerramos conexión estructural antes de la simulación
        conn.close()
        
        # 3. Lanzamos el poblador de la base de datos
        # Generará 500 clientes y simulará 2,500 transferencias instantáneas en este caso
        poblar_sistema_fintech(total_clientes=500, total_transacciones=2500)
        
        print("Proceso terminado. Base de datos lista.")
        
    except Exception as e:
        print(f"Error crítico en el despliegue: {e}")