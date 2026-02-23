import psycopg2
from psycopg2 import Error


def obtener_conexion():
    """Mantenemos la conexión simple para este paquete"""
    return psycopg2.connect(
        host="localhost",
        dbname="banco_db",
        user="postgres",
        password="cqr"
    )


def realizar_transferencia_pro(origen, destino, cantidad):
    """
    Transferencia avanzada usando Context Managers (with).
    Este estilo reduce el código 'boilerplate' y aumenta la seguridad.
    """
    try:
        # El primer 'with' gestiona la transacción (commit/rollback)
        with obtener_conexion() as conn:
            # El segundo 'with' gestiona el cursor (cierre automático)
            with conn.cursor() as cur:
                print(f"Iniciando transferencia de {cantidad}€...")

                # 1. Restar saldo (Seguridad v2 + Transacción v3)
                cur.execute(
                    "UPDATE cuentas SET saldo = saldo - %s WHERE numero_cuenta = %s",
                    (cantidad, origen)
                )

                # 2. Sumar saldo
                cur.execute(
                    "UPDATE cuentas SET saldo = saldo + %s WHERE numero_cuenta = %s",
                    (cantidad, destino)
                )

                # Con psycopg2, al salir del bloque 'with conn',
                # se hace COMMIT automáticamente si no hubo errores.
                print("Operaciones ejecutadas con éxito.")

    except (Exception, Error) as e:
        print(f"TRANSACCIÓN ABORTADA: Se ha realizado rollback automático.")
        print(f"Razón: {e}")


# --- Bloque de prueba ---
if __name__ == "__main__":
    # Escenario de éxito
    realizar_transferencia_pro("111", "222", 50.0)