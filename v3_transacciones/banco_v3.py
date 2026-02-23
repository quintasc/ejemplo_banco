import psycopg2
from psycopg2 import Error


def obtener_conexion():
    return psycopg2.connect(
        host="localhost",
        dbname="banco_db",
        user="postgres",
        password="cqr"
    )


def realizar_transferencia(origen, destino, cantidad):
    """
    Implementación de transferencia con control de transacciones.
    Garantiza que el dinero no se pierda si falla la segunda operación.
    """
    conn = obtener_conexion()
    cur = conn.cursor()

    try:
        # 1. Restar dinero de la cuenta origen
        # Usamos parámetros %s para mantener la seguridad de la v2
        cur.execute(
            "UPDATE cuentas SET saldo = saldo - %s WHERE numero_cuenta = %s",
            (cantidad, origen)
        )

        # Simulamos un posible error (ej. caída de red o error de lógica)
        # if cantidad > 1000: raise Exception("Error simulado: Límite excedido")

        # 2. Sumar dinero a la cuenta destino
        cur.execute(
            "UPDATE cuentas SET saldo = saldo + %s WHERE numero_cuenta = %s",
            (cantidad, destino)
        )

        # Si ambas operaciones tuvieron éxito, grabamos los cambios permanentemente
        conn.commit()
        print("Transferencia realizada con éxito y confirmada (COMMIT).")

    except (Exception, Error) as error:
        # Si algo falla, deshacemos cualquier cambio pendiente
        conn.rollback()
        print(f"ERROR: La transferencia ha fallado. Se ha restaurado el saldo (ROLLBACK).")
        print(f"Detalle: {error}")

    finally:
        # Cerramos siempre los recursos
        cur.close()
        conn.close()


# --- Bloque de prueba
if __name__ == "__main__":
    # Escenario: Transferencia de Carme (111) a Admin (222)
    print("Iniciando transferencia segura...")
    realizar_transferencia("111", "222", 100.0)