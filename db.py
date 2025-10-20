import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
load_dotenv()
import os

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_DATABASE")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

def connect():
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )

        print("Conexão foi um sucesso ")
        return conn

    except Error as e:
        print(f"Ocorreu um erro {e}")
        return None


def close(conn, cursor=None):
    if conn:
        conn.close()
    if cursor:
        cursor.close()
    print("Conexão encerrada")

teste = connect()
teste