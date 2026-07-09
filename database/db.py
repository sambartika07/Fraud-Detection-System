import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        port="2347",
        database="fraudguard",
        user="postgres",
        password="sam123"
    )
    return conn