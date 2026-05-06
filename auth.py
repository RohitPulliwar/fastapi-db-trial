import psycopg2



def get_db():
    conn = psycopg2.connect(
    dbname="student_db",
    user="postgres",
    password="shilpamohan2425",
    host="localhost",
    port="5432"
)
    return conn