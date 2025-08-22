from dotenv import load_dotenv
from psycopg2 import pool
import os

load_dotenv()

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

try:
    db_pool = pool.SimpleConnectionPool(
        minconn = 1,
        maxconn = 10,
        dbname = db_name,
        user = db_user,
        password = db_password,
        host = db_host,
        port = db_port
    )
    print("Database connection pool created successfully.")
except:
    print("Error creating connection pool!")
    raise SystemExit("Exiting...")


def get_connection():
    try:
        return db_pool.getconn()
    except:
        print("Failed to get database connection!")
        raise SystemExit("Exiting...")

def release_connection(conn):
    try:
        db_pool.putconn(conn)
    except:
        print("Failed to release database connection!")
        raise SystemExit("Exiting...")

def close_all_connections():
    db_pool.closeall()
    print("All database connections closed...")
