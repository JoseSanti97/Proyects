import random
from decimal import Decimal
from faker import Faker
from sqlalchemy.orm import Session
from generador.modelos import Cliente, Cliente_Tel, Cuenta, Tarjeta, Transaccion, Prestamo, Beneficiario, Beneficiario_Tel

fake = Faker('es_MX')

TIPOS_CUENTA = ["Debito", "Ahorro", "Nomina", "Chequera"]
ESTADOS_TARJETA = ["Activa", "Bloqueada", "Vencida"]
TIPOS_MOVIMIENTO = ["Deposito", "Retiro", "Transferencia", "Pago de Servicio"]
PARENTESCOS = ["Hijo/a", "Esposo/a", "Madre", "Padre", "Hermano/a"]
ESTADOS_PRESTAMO = ["Activo", "Pagado", "Vencido", "En Mora"]
EMISORES_TARJETA = ["Visa", "Mastercard", "American Express"]
ESTADOS_CIVILES = ['casado/a', 'soltero/a', 'viudo/a']

DELEGACIONES_CDMX = [
    "Alvaro Obregon", "Azcapotzalco", "Benito Juarez", "Coyoacan", "Cuajimalpa",
    "Cuauhtemoc", "Gustavo A. Madero", "Iztacalco", "Iztapalapa", "Magdalena Contreras",
    "Miguel Hidalgo", "Milpa Alta", "Tlahuac", "Tlalpan", "Venustiano Carranza", "Xochimilco"
]

def poblar_sistema(session: Session, total_clientes: int = 5000, transacciones_por_cliente: int = 5):
    print(f"Iniciando registro de {total_clientes} clientes y sus dependencias")

    for i in range(total_clientes):
        
        # 1.- Generar información del cliente
        new_curp = fake.bothify(text='????######??????##').upper() 
        nuevo_cliente = Cliente(
            nombre=fake.first_name(),
            apellido=fake.last_name(),
            curp=new_curp,
            correo=fake.unique.email(),
            estado_civil=random.choice(ESTADOS_CIVILES),
            delegacion=random.choice(DELEGACIONES_CDMX)
        )

        session.add(nuevo_cliente)
        session.flush() 

        # 2.- Generar los teléfonos del cliente
        nuevo_tel = Cliente_Tel(
            tel=fake.unique.bothify(text='55########'), 
            id_cliente=nuevo_cliente.id_cliente 
        )
        session.add(nuevo_tel)

        # 3.- Generación de al menos una cuenta bancaria por cliente
        no_cuenta_creada = fake.unique.bothify(text='############') 
        new_cuenta = Cuenta(
            no_cuenta=no_cuenta_creada,
            tipo_cuenta=random.choice(TIPOS_CUENTA), 
            saldo=Decimal(round(random.uniform(1000.0, 1000000.0), 2)),
            id_cliente=nuevo_cliente.id_cliente 
        )
        session.add(new_cuenta)
        session.flush() 
        
        # 4.- Generación de los beneficiarios
        new_beneficiario = Beneficiario(
            parentesco=random.choice(PARENTESCOS),
            nombre=fake.first_name(),
            apellido=fake.last_name(),
            porcentaje_saldo=Decimal('100.00'),
            no_cuenta=new_cuenta.no_cuenta
        )
        session.add(new_beneficiario)
        session.flush()

        # 5.- Generación de los teléfonos del beneficiario
        new_tel = Beneficiario_Tel(
            tel=fake.unique.bothify(text='55########'),
            id_beneficiario=new_beneficiario.id_beneficiario
        )
        session.add(new_tel)
        session.flush()

        # 5.- Generar la tarjeta asociada a la cuenta (Paso indispensable para las transacciones)
        no_tarjeta_creada = fake.unique.bothify(text='4152############')
        nueva_tarjeta = Tarjeta(
            no_tarjeta=no_tarjeta_creada,
            cvv=fake.bothify(text='###'),
            emisor=random.choice(EMISORES_TARJETA),
            estado=random.choice(ESTADOS_TARJETA),
            no_cuenta=new_cuenta.no_cuenta
        )
        session.add(nueva_tarjeta)
        session.flush()

        # 6.- Generar transacciones asociadas a la tarjeta
        for _ in range(transacciones_por_cliente): 
            new_transaccion = Transaccion(
                no_tarjeta=nueva_tarjeta.no_tarjeta,
                cuenta_origen=new_cuenta.no_cuenta,
                cuenta_destino=fake.bothify(text='############'),
                monto=Decimal(round(random.uniform(50.0, 5000.0), 2)),
                tipo_movimiento=random.choice(TIPOS_MOVIMIENTO),
                fecha_transaccion=fake.date_time_between(start_date='-30d', end_date='now')
            )
            session.add(new_transaccion)

        # 7.- Generar un préstamos con menos del 20% de probabilidad de que ocurran
        if random.random() < 0.20:
            new_prestamo = Prestamo(
                estado=random.choice(ESTADOS_PRESTAMO),
                monto=Decimal(round(random.uniform(5000.0, 150000.0), 2)),
                id_cliente=nuevo_cliente.id_cliente
            )
            session.add(new_prestamo) 

    # Al terminar loop, se hace el commit final
    try:
        print("Confirmación y guardado en la base de datos")
        session.commit()
        print("Proceso completado con éxito. Los registros han sido realizados.")
    except Exception as e:
        print(f"Error, aplicando Rollback. Motivo: {e}")
        session.rollback() 
        raise e