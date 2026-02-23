import psycopg2


def obtener_conexion():
    return psycopg2.connect(
        host="localhost",
        dbname="banco_db",
        user="postgres",
        password="cqr"
    )

def alta_cuenta(numero, titular, saldo):
    """Alta de cuenta usando concatenación (Vulnerable a SQL Injection)"""
    conn = obtener_conexion()
    cur = conn.cursor()
    # ERROR CRÍTICO: El uso de f-strings para insertar datos permite ataques de inyección
    query = f"INSERT INTO cuentas (numero_cuenta, titular, saldo) VALUES ('{numero}', '{titular}', {saldo})"
    print(f"Ejecutando SQL: {query}")
    cur.execute(query)
    conn.commit()
    conn.close()
    print("Cuenta creada con éxito.")


def baja_cuenta(numero):
    """Baja de cuenta (Vulnerable)"""
    conn = obtener_conexion()
    cur = conn.cursor()
    query = f"DELETE FROM cuentas WHERE numero_cuenta = '{numero}'"
    cur.execute(query)
    conn.commit()
    conn.close()
    print(f"Cuenta {numero} eliminada.")


def consultar_saldo(numero):
    """Consulta de saldo (Vulnerable)"""
    conn = obtener_conexion()
    cur = conn.cursor()
    # ERROR CRÍTICO: Vulnerable a Inyección SQL [cite: 18]
    query = f"SELECT titular, saldo FROM cuentas WHERE numero_cuenta = '{numero}'"
    print(f"Ejecutando consulta: {query}")
    cur.execute(query)
    # resultado = cur.fetchone()
    resultado = cur.fetchall()
    conn.close()
    return resultado


def realizar_ingreso(numero, cantidad):
    """Ingreso de dinero (Sin transacciones)"""
    conn = obtener_conexion()
    cur = conn.cursor()
    query = f"UPDATE cuentas SET saldo = saldo + {cantidad} WHERE numero_cuenta = '{numero}'"
    cur.execute(query)
    conn.commit()
    conn.close()


def realizar_reintegro(numero, cantidad):
    """Reintegro de dinero (Sin control de errores ni transacciones)"""
    conn = obtener_conexion()
    cur = conn.cursor()
    query = f"UPDATE cuentas SET saldo = saldo - {cantidad} WHERE numero_cuenta = '{numero}'"
    cur.execute(query)
    conn.commit()
    conn.close()


def realizar_transferencia(origen, destino, cantidad):
    """Transferencia (ERROR: Sin atomicidad/transacciones)"""
    conn = obtener_conexion()
    cur = conn.cursor()
    # Si falla la segunda operación, el dinero de la primera se pierde
    query1 = f"UPDATE cuentas SET saldo = saldo - {cantidad} WHERE numero_cuenta = '{origen}'"
    query2 = f"UPDATE cuentas SET saldo = saldo + {cantidad} WHERE numero_cuenta = '{destino}'"
    cur.execute(query1)
    cur.execute(query2)
    conn.commit()
    conn.close()


# --- Bloque de prueba
if __name__ == "__main__":
    # 1. Alta normal
    # alta_cuenta("123", "Alumno Monlau", 100.0)
    print("Resultado consulta normal1:", consultar_saldo("111"))
    print("Resultado consulta normal2:", consultar_saldo("123"))
    # 2. Prueba de ataque de Inyección SQL:
    # Si el usuario introduce lo siguiente en 'numero': 123' OR '1'='1
    print("Resultado consulta maliciosa:", consultar_saldo("123' OR '1'='1"))