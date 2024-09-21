import requests
import psycopg2
from src.DBManager import DBManager
# from src.utils import
from config import CONN

try:
    with CONN:
        with CONN.cursor() as cur:
            # работа с базой данных, вызовы команд в бд через курсор
            pass

finally:
    CONN.close()