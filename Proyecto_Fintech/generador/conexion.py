import psycopg2

def obtener_conexion():
    """Establece y retorna la conexión con el contenedor de PostgreSQL en Docker."""
    return psycopg2.connect(
        host="localhost",
        database="Tu base de datos",        
        user="Tu nombre de usuario",          
        password="Tu passwordd",    
        port="5432"
    )