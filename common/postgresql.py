import psycopg2
from _United import settings

dbSettings = settings.DATABASES["default"]

connectionPG = psycopg2.connect(
    user=dbSettings["USER"],
    password=dbSettings["PASSWORD"],
    host=dbSettings["HOST"],
    port=dbSettings["PORT"],
    database=dbSettings["NAME"],
)

cursorDB = connectionPG.cursor()

