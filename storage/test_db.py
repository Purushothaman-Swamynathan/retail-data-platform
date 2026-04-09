from db import get_connection

conn = get_connection()

if conn:
    print("SUCCESS: DB is working")
    conn.close()