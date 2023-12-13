import psycopg2

connectionPG = psycopg2.connect(
    user="philong249",
    password="01886933234",
    host="localhost",
    port="5432",
    database="plpostgres_database",
)

cursorDB = connectionPG.cursor()