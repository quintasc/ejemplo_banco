from .db_connection import DBConnection
from psycopg2 import Error

class CuentaDAO:
    """Data Access Object para la tabla 'cuentas'."""

    def __init__(self):
        # Obtenemos la instancia única de conexión
        self.db = DBConnection().get_connection()

    def consultar_cuenta(self, numero):
        """Consulta segura y profesional usando parámetros."""
        with self.db.cursor() as cur:
            query = "SELECT titular, saldo FROM cuentas WHERE numero_cuenta = %s"
            cur.execute(query, (numero,))
            return cur.fetchone()

    def transferencia_bancaria(self, origen, destino, cantidad):
        """Implementación profesional con Transacciones y Context Managers."""
        try:
            # Al usar 'with self.db', psycopg2 gestiona el COMMIT/ROLLBACK automáticamente
            with self.db:
                with self.db.cursor() as cur:
                    # 1. Restar de origen
                    cur.execute(
                        "UPDATE cuentas SET saldo = saldo - %s WHERE numero_cuenta = %s",
                        (cantidad, origen)
                    )
                    # 2. Sumar a destino
                    cur.execute(
                        "UPDATE cuentas SET saldo = saldo + %s WHERE numero_cuenta = %s",
                        (cantidad, destino)
                    )
            print(f"Transferencia de {cantidad}€ completada con éxito.")
            return True
        except Exception as e:
            print(f"La transferencia falló en el DAO: {e}")
            # El rollback es automático gracias al context manager del Singleton
            return False

    def alta_cuenta(self, numero, titular, saldo):
        try:
            with self.db:
                with self.db.cursor() as cur:
                    query = "INSERT INTO cuentas (numero_cuenta, titular, saldo) VALUES (%s, %s, %s)"
                    cur.execute(query, (numero, titular, saldo))
            return True
        except Error:
            return False