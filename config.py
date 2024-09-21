import psycopg2


CONN = psycopg2.connect(
    host="localhost",
    database="db_hh",
    user="postgres",
    password="456776"
)