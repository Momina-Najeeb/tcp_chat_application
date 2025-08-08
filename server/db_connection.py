from psycopg2 import pool

db_name = "chat_app"
db_user = "postgres"
db_password = "Admin"
db_host = "localhost"
db_port = "5432"

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
        db_pool.getconn()
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
