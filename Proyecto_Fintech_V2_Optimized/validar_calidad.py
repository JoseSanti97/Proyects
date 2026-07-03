import sys
from sqlalchemy import text
from generador.conexion import obtener_sesion

def exec_test():
    print("[DATA QUALITY] Iniciando pruebas de calidad y consistencia de datos")
    session = obtener_sesion()
    if not session:
        sys.exit(1)

    tests = {
        "1. Cuentas con saldos negativos (Debe ser 0)": 
            "SELECT COUNT(*) FROM cuenta WHERE saldo < 0;",
        
        "2. Transacciones con monto cero o negativo (Debe ser 0)": 
            "SELECT COUNT(*) FROM transaccion WHERE monto <= 0;",
        
        "3. Clientes huérfanos sin ninguna cuenta asignada (Debe ser 0)": 
            "SELECT COUNT(*) FROM cliente c LEFT JOIN cuenta cu ON c.id_cliente = cu.id_cliente WHERE cu.no_cuenta IS NULL;",
        
        "4. Beneficiarios cuyo porcentaje asignado NO sume 100% por cuenta (Debe ser 0)": 
            "SELECT COUNT(*) FROM (SELECT no_cuenta, SUM(porcentaje_saldo) as total FROM beneficiario GROUP BY no_cuenta) as b WHERE b.total != 100.00;"
    }

    errors_found = 0

    try:
        for name_test, query in tests.items():
            result = session.execute(text(query)).scalar()
            if result == 0:
                print(f"Pasó: {name_test}")
            else:
                print(f"Fracaso ({result} resgistros corruptos): {name_test}")
            