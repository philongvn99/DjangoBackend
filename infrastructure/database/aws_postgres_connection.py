import psycopg2

from _United import settings

dbSettings = settings.DATABASES["default"]

try:
    connectionPG = psycopg2.connect(
        user=dbSettings["USER"],
        password=dbSettings["PASSWORD"],
        host=dbSettings["HOST"],
        port=dbSettings["PORT"],
        database=dbSettings["NAME"],
    )

    cursorDB = connectionPG.cursor()
except psycopg2.Error as e:
    print(e)
