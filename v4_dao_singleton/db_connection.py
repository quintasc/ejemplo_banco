import psycopg2
from psycopg2 import Error

class DBConnection:
    """Clase Singleton para gestionar la conexión única a banco_db."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            try:
                cls._instance = super(DBConnection, cls).__new__(cls)
                # En un entorno profesional, estos datos vendrían de un .env
                cls._instance.connection = psycopg2.connect(
                    host="localhost",
                    dbname="banco_db",
                    user="postgres",
                    password="cqr"
                )
                print("Conexión a la base de datos establecida con éxito (Singleton).")
            except Error as e:
                print(f"Error al conectar a la base de datos: {e}")
                cls._instance = None
        return cls._instance

    def get_connection(self):
        return self.connection