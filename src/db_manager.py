import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()


# conn = os.getenv("CONN")
class DBManager:
    """Класс для работы с базой данных PostgreSQL"""

    def __init__(self, database_name):
        self._database_name = database_name

    def execute_query(self, query):
        """Подключаемся к базе данных"""
        conn = psycopg2.connect(database_name='postgres', user=os.getenv("user"), password=os.getenv("password"),
                                host=os.getenv("host"), port=os.getenv("port"))
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()
        return result

    def get_companies_and_vacancies_count(self):
        """получаем список всех компаний и количество вакансий у каждой компании"""
        query = ("SELECT employer.id, employer.name, COUNT(vacancy.id) AS vacancy_count "
                 "FROM employer "
                 "LEFT JOIN vacancy ON employer.id = vacancy.employer_id "
                 "GROUP BY employer.id, employer.name "
                 "ORDER BY employer.name")
        return self.execute_query(query)

    def get_all_vacancies(self):
        """получаем список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию"""
        return self.execute_query("SELECT * FROM vacancy")

    def get_avg_salary(self):
        """получаем среднюю зарплату по вакансиям"""
        return self.execute_query("SELECT AVG(salary_from) FROM vacancy")

    def get_vacancies_with_higher_salary(self):
        """получаем список всех вакансий, у которых зарплата выше средней
        по всем вакансиям"""
        return self.execute_query("SELECT name, salary_from, url FROM vacancy "
                                    "WHERE salary_from > (SELECT AVG(salary_from) FROM vacancy)")

    def get_vacancies_with_keyword(self, keyword):
        """получаем список всех вакансий, в названии которых содержатся
        переданные в метод слова, например, python"""
        query = f"SELECT * FROM vacancy WHERE name LIKE '%{keyword}%'"
        return self.execute_query(query)
