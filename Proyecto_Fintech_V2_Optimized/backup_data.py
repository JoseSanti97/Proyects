import os
import subprocess
from datetime import datetime

def respaldar_base_de_datos():
    print("[INFRAESTRUCTURA] Iniciando respaldo automático de la base de datos")
    
    # Configuración basada en tus credenciales de Docker
    archivo_salida = f"backup_fintech_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    
    # Ejecutamos el comando pg_dump DIRECTAMENTE dentro de tu contenedor de Docker
    comando = f"docker exec -t bd_nombre pg_dump -U tu_usuario -d tu_db > {archivo_salida}"
    
    try:
        # Ejecuta el comando en la terminal del sistema operativo
        subprocess.run(comando, shell=True, check=True)
        print(f"[ÉXITO] Respaldo generado correctamente en el archivo local: {archivo_salida}")
    except subprocess.CalledProcessError as e:
        print(f"[FALLO] No se pudo realizar el respaldo. Verifica que el contenedor Docker esté activo. Motivo: {e}")

if __name__ == "__main__":
    respaldar_base_de_datos()