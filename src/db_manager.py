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
        conn = psycopg2.connect(dbname=self._database_name, user=os.getenv("user"), password=os.getenv("password"),
                                host=os.getenv("host"), port=os.getenv("port"))
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()
        return result

    def get_companies_and_vacancies_count(self):
        """получаем список всех компаний и количество вакансий у каждой компании"""
        query = ("SELECT employers.id, employers.name, employers.all_vacancies "
                 "FROM employers "
                 "LEFT JOIN vacancies ON employers.id = vacancies.employer_id "
                 "GROUP BY employers.id, employers.name "
                 "ORDER BY employers.name "
                 "LIMIT 10")
        return self.execute_query(query)


    def get_all_employers(self):
        """получаем список всех вакансий с указанием  компании, зарплаты и ссылки на вакансию """
        return self.execute_query("SELECT * FROM vacancies LIMIT 10")


    def get_all_vacancies(self):
        """получаем список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию"""
        return self.execute_query("SELECT * FROM vacancies LIMIT 10")

    def get_avg_salary(self):
        """получаем среднюю зарплату по вакансиям"""
        return self.execute_query("SELECT AVG(salary_from) FROM vacancies LIMIT 10")

    def get_vacancies_with_higher_salary(self):
        """получаем список всех вакансий, у которых зарплата выше средней
        по всем вакансиям"""
        return self.execute_query("SELECT name, salary_from, url FROM vacancies "
                                    "WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies) LIMIT 10")

    def get_vacancies_with_keyword(self, keyword):
        """получаем список всех вакансий, в названии которых содержатся
        переданные в метод слова, например, python"""
        query = f"SELECT * FROM vacancies WHERE name LIKE '%{keyword}%'"
        return self.execute_query(query)
