import random
from datetime import datetime, timedelta
from faker import Faker
import psycopg2
from generador.conexion import obtener_conexion

# Inicializamos Faker
fake = Faker('es_MX')

def poblar_sistema_fintech(total_clientes=500, total_transacciones=2500):
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    print(f"\n👥 Fabricando {total_clientes} clientes con sus productos financieros")

    lista_id_clientes = []
    lista_cuentas = []
    lista_tarjetas = []

    # =========================================================================
    # PASO 1: INSERTAR CLIENTES, TELÉFONOS, BIOMETRÍA Y CUENTAS
    # =========================================================================
    for _ in range(total_clientes):
        # 1. Crear registro en CLIENTE
        curp = fake.unique.bothify(text='????######??????##').upper()
        nacionalidad = "Mexicana"
        estado_civil = random.choice(['Soltero', 'Casado', 'Divorciado', 'Viudo'])
        
        cursor.execute("""
            INSERT INTO CLIENTE (CURP, Nacionalidad, Estado_Civil)
            VALUES (%s, %s, %s) RETURNING ID_Cliente;
        """, (curp, nacionalidad, estado_civil))
        id_cliente = cursor.fetchone()[0]
        lista_id_clientes.append(id_cliente)

        # 2. Crear teléfono asociado
        telefono = fake.bothify(text='55########')
        cursor.execute("""
            INSERT INTO CLIENTE_TEL (Tel, ID_Cliente)
            VALUES (%s, %s);
        """, (telefono, id_cliente))

        # 3. Crear biometría asociada
        tipo_bio = random.choice(['Huella Dactilar', 'Rostro', 'Iris'])
        hash_ref = fake.sha256(raw_output=False)
        cursor.execute("""
            INSERT INTO CLIENTE_BIOMETRIA (Tipo_Biometria, Hash_referencia, ID_Cliente)
            VALUES (%s, %s, %s);
        """, (tipo_bio, hash_ref, id_cliente))

        # 4. Crear Cuenta bancaria
        no_cuenta = f"{curp[:4]}{random.randint(100000, 999999)}"
        tipo_cuenta = random.choice(['Ahorro', 'Corriente', 'Nomina'])
        saldo_inicial = round(random.uniform(2000.0, 75000.0), 2)
        
        cursor.execute("""
            INSERT INTO CUENTA (No_Cuenta, Tipo_Cuenta, Saldo, Tarjetas_Asociadas, ID_Cliente)
            VALUES (%s, %s, %s, 0, %s);
        """, (no_cuenta, tipo_cuenta, saldo_inicial, id_cliente))
        lista_cuentas.append(no_cuenta)

        # 5. Crear Tarjeta con 80% de probabilidad
        if random.random() < 0.80:
            no_tarjeta = fake.credit_card_number(card_type='visa')[:16]
            cvv = fake.bothify(text='###')
            emisor = random.choice(['Visa', 'Mastercard'])
            estado_tarjeta = 'Activa'
            
            cursor.execute("""
                INSERT INTO TARJETA (No_Tarjeta, CVV, Emisor, Estado, No_Cuenta)
                VALUES (%s, %s, %s, %s, %s);
            """, (no_tarjeta, cvv, emisor, estado_tarjeta, no_cuenta))
            lista_tarjetas.append(no_tarjeta)
            
            # Sumamos 1 al contador de tarjetas de la cuenta
            cursor.execute("""
                UPDATE CUENTA SET Tarjetas_Asociadas = Tarjetas_Asociadas + 1 WHERE No_Cuenta = %s;
            """, (no_cuenta,))

    conn.commit()
    print("✅ Entidades base integradas correctamente.")
    
    # =========================================================================
    # PASO 2: SIMULAR LOS MOVIMIENTOS (RETIROS, DEPÓSITOS, TRANSACCIONES) 
    # =========================================================================
    print(f"💸 Procesando ráfaga de {total_transacciones} transacciones aleatorias")
    exitosas = 0
    rechazadas = 0

    for _ in range(total_transacciones):
        cuenta_origen = random.choice(lista_cuentas)
        cuenta_destino = random.choice(lista_cuentas)
        
        # Evitar transferencia a sí mismo
        while cuenta_destino == cuenta_origen:
            cuenta_destino = random.choice(lista_cuentas)
            
        monto = round(random.uniform(10.0, 2000.0), 2)
        tipo_movimiento = random.choice(['Transferencia', 'Pago de Servicio', 'Retiro'])
        tarjeta_usada = random.choice(lista_tarjetas) if random.random() < 0.50 else None
        fecha_aleatoria = datetime.now() - timedelta(days=random.randint(0, 150))

        try:
            # Intentamos insertar el movimiento
            cursor.execute("""
                INSERT INTO TRANSACCION (Cuenta_Destino, Cuenta_Origen, Monto, Tipo_Movimiento, FECHA, No_Tarjeta)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (cuenta_destino, cuenta_origen, monto, tipo_movimiento, fecha_aleatoria, tarjeta_usada))
            exitosas += 1
            
        except psycopg2.InternalError:
            # TRIGGER de saldo insuficiente frena la operación
            conn.rollback()
            rechazadas += 1
            continue

    conn.commit()
    cursor.close()
    conn.close()
    
    # Imprimir resumen de la prueba de estrés
    print("\n📊 === RESULTADOS DEL REGISTRO ===")
    print(f" Clientes y Cuentas creados: {total_clientes}")
    print(f" Transacciones liquidadas con éxito: {exitosas}")
    print(f" Intentos rechazados (Sin Saldo): {rechazadas}")
    print("============================================\n")