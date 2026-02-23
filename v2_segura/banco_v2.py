import psycopg2
from psycopg2 import Error


def obtener_conexion():
    return psycopg2.connect(
        host="localhost",
        dbname="banco_db",
        user="postgres",
        password="cqr"
    )


def alta_cuenta(numero, titular, saldo):
    """Alta segura usando parámetros %s"""
    conn = obtener_conexion()
    cur = conn.cursor()
    # Los %s son marcadores de posición, no concatenación de strings
    query = "INSERT INTO cuentas (numero_cuenta, titular, saldo) VALUES (%s, %s, %s)"
    # Los datos se pasan como una TUPLA en el segundo argumento de execute()
    cur.execute(query, (numero, titular, saldo))
    conn.commit()
    conn.close()
    print(f"Cuenta de {titular} creada de forma segura.")


def consultar_saldo(numero):
    """Consulta segura: El motor trata el input como simple texto"""
    conn = obtener_conexion()
    cur = conn.cursor()
    query = "SELECT titular, saldo FROM cuentas WHERE numero_cuenta = %s"
    print(f"Ejecutando consulta parametrizada para: {numero}")

    # El driver 'psycopg2' se encarga de limpiar (escapar) el contenido de 'numero'
    # Si se ejecuta: consultar_saldo("123' OR '1'='1") el driver escapará las
    # comillas de forma que lo que se buscará es una cuenta con un valor de numero_cuenta
    # que coincida exactamente con el literal "123' OR '1'='1"
    cur.execute(query, (numero,))
    resultado = cur.fetchone()
    conn.close()
    return resultado


def realizar_transferencia(origen, destino, cantidad):
    """Transferencia segura pero todavía SIN transacciones (se verá en v3)"""
    conn = obtener_conexion()
    cur = conn.cursor()
    query_restar = "UPDATE cuentas SET saldo = saldo - %s WHERE numero_cuenta = %s"
    query_sumar = "UPDATE cuentas SET saldo = saldo + %s WHERE numero_cuenta = %s"

    cur.execute(query_restar, (cantidad, origen))
    cur.execute(query_sumar, (cantidad, destino))

    conn.commit()
    conn.close()


# --- Bloque de prueba para alumnos ---
if __name__ == "__main__":
    # 1. Intento de ataque de Inyección SQL:
    # Si el usuario introduce: 123' OR '1'='1
    print("Intentando hackear v2...")
    ataque = "123' OR '1'='1"
    resultado = consultar_saldo(ataque)

    if resultado:
        print(f"Resultado: {resultado}")
    else:
        # Ahora el resultado será None porque busca LITERALMENTE la cuenta "123' OR '1'='1"
        print("Ataque fallido: La consulta parametrizada ha neutralizado la inyección.")


realizar_transferencia("111", "333", 50)
resultado = consultar_saldo("111")

if resultado:
    print(f"Resultado: {resultado}")
else:
    print("La cuenta no existe en la base de datos.")

resultado = consultar_saldo("333")

if resultado:
    print(f"Resultado: {resultado}")
else:
    # Ahora el resultado será None porque "123" no existe
    print("La cuenta no existe en la base de datos.")
