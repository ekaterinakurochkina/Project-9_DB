import requests
import psycopg2
import os
from dotenv import load_dotenv
from src.api_access import ApiWork


load_dotenv()

def create_database(database_name: str):
    """Создание базы данных с таблицами для сохранения данных о вакансиях и работодателях."""

    conn = psycopg2.connect(dbname='postgres', user=os.getenv("user"), password=os.getenv("password"),
                            host=os.getenv("host"), port=os.getenv("port"))
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name} WITH (FORCE)")
    cur.execute(f"CREATE DATABASE {database_name}")
    cur.close()
    conn.close()

def create_tables(database_name):
    """Создание таблиц работодателей и вакансий"""
    conn = psycopg2.connect(dbname=database_name, user=os.getenv("user"), password=os.getenv("password"),
                            host=os.getenv("host"), port=os.getenv("port"))
    with conn:
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE employers (
            id INTEGER PRIMARY KEY,
            all_vacancies INT,
            name VARCHAR(255) NOT NULL UNIQUE)""")

            cur.execute("""CREATE TABLE vacancies (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            salary_from INTEGER,
            salary_to INTEGER,
            url VARCHAR(255),
            employer_id INTEGER REFERENCES employers(id) NOT NULL)""")
    conn.close()


def insert_data_to_database(database_name):
    """Функция сохранения данных о работодателях и вакансиях
    в базу данных"""
    conn = psycopg2.connect(dbname=database_name, user=os.getenv("user"), password=os.getenv("password"),
                            host=os.getenv("host"), port=os.getenv("port"))

    with conn:
        with conn.cursor() as cur:
            hh = ApiWork()
            employers = hh.get_employers()
            for employer in employers:
                employer_id = employer["id"]
                all_vacancies = employer["open_vacancies"]
                cur.execute("INSERT INTO employers VALUES (%s, %s, %s)", (employer_id, all_vacancies, employer["name"]))
                vacansies = hh.get_vacancies(employer_id)
                for vacancy in vacansies:
                    if not vacancy["salary"]:  # Если зарплата не указана, в таблице будут нули
                        salary_from = 0
                        salary_to = 0
                    else:
                        salary_from = vacancy["salary"]["from"] if vacancy["salary"]["from"] else 0
                        salary_to = vacancy["salary"]["to"] if vacancy["salary"]["to"] else 0

                    cur.execute("INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)", (vacancy["id"], vacancy["name"],
                                                                                        salary_from, salary_to,
                                                                                        vacancy["alternate_url"],
                                                                                        employer_id))
    conn.close()
