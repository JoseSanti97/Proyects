import psycopg2

def obtener_conexion():
    """Establece y retorna la conexión con el contenedor de PostgreSQL en Docker."""
    return psycopg2.connect(
        host="localhost",
        database="postgres",        
        user="postgres",          
        password="AdminPass123",    
        port="5432"
    )