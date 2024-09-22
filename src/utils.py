import requests
import psycopg2
import os

def create_database(database_name: str, params: dict):
    """Создание базы данных с таблицами для сохранения данных о вакансиях и работодателях."""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name} WITH (FORCE)")
    cur.execute(f"CREATE DATABASE {database_name}")
    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (    # работодатели
            id INTEGER PRIMARY KEY,
            all_vacancies INT,
            name VARCHAR(255) NOT NULL UNIQUE
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            salary_from INTEGER,
            salary_to INTEGER,
            url VARCHAR(255),
            employer_id INTEGER REFERENCES employer(id) NOT NULL
            )
        """)

    conn.commit()
    conn.close()


def insert_data_to_database(data, db_name):
    """Функция сохранения данных о работодателях и вакансиях
    в базу данных"""
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in data:


    with conn:
        with conn.cursor() as cur:
            hh = HHParser()
            employers = hh.get_employers()
            for employer in employers:
                employer_id = employer["id"]
                cur.execute(
                    "INSERT INTO employer VALUES (%s, %s)",
                    (employer_id, employer["name"]),
                )
                vacansies = hh.get_vacancies(employer_id)
                for vacancy in vacansies:
                    if not vacancy[
                        "salary"
                    ]:  # Если зарплата не указана, заполняем нули
                        salary_from = 0
                        salary_to = 0
                    else:
                        salary_from = (
                            vacancy["salary"]["from"]
                            if vacancy["salary"]["from"]
                            else 0
                        )
                        salary_to = (
                            vacancy["salary"]["to"] if vacancy["salary"]["to"] else 0
                        )

                    cur.execute(
                        "INSERT INTO vacancy VALUES (%s, %s, %s, %s, %s, %s)",
                        (
                            vacancy["id"],
                            vacancy["name"],
                            salary_from,
                            salary_to,
                            vacancy["alternate_url"],
                            employer_id,
                        ),
                    )
    conn.close()
