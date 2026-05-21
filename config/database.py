import psycopg2


def get_db_connection():
    return psycopg2.connect(
        dbname="ai_middleware",
        user="middleware_user",
        password="middleware123",
        host="localhost",
        port="5432"
    )