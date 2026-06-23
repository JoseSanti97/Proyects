import psycopg2

def obtener_conexion():
    """Establece y retorna la conexión con el contenedor de PostgreSQL en Docker."""
    return psycopg2.connect(
        host="localhost",
        database="nombre de tu DB",        
        user="Nombre de usuario",          
        password="Tu password",    
        port="5432"
    )