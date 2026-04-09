import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname="retail_db",
            user="postgres",
            password="root",   # change if different
            host="localhost",
            port="5432"
        )
        print("Database connected successfully")
        return conn

    except Exception as e:
        print("Error connecting to database:", e)