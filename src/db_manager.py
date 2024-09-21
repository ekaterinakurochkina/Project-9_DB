import psycopg2
from config import CONN

class DBManager():
    """Класс для работы с базой данных PostgreSQL"""
    def __init__(self, params):
        self.conn = psycopg2.connect(dbname='db_hh', **params)
        self.cur = self.conn.cursor()


    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании"""
        self.cur.execute(f"SELECT company_name, open_vacancies FROM employers")
        return self.cur.fetchall()


    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании,
                названия вакансии и зарплаты и ссылки на вакансию"""
        self.cur.execute(
            f"SELECT employers.company_name, vacancies.vacancy_name, vacancies.salary_from, vacancies.vacancy_url FROM vacancies "
            f"JOIN employers USING(employer_id)")
        return self.cur.fetchall()


    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям"""
        self.cur.execute(f"SELECT AVG(salary_from) FROM vacancies")
        return self.cur.fetchall()


    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней
        по всем вакансиям"""
        self.cur.execute(f"SELECT vacancy_name, salary_from FROM vacancies "
                         f"GROUP BY vacancy_name, salary_from HAVING salary_from > (select avg(salary_from) FROM vacancies)"
                         f"ORDER BY salary_from")
        return self.cur.fetchall()


    def get_vacancies_with_keyword(self, word):
        """получает список всех вакансий, в названии которых содержатся
        переданные в метод слова, например, python"""
        q = """SELECT * FROM vacancies WHERE LOWER(vacancy_name) LIKE %s"""
        self.cur.execute(q, ('%' + word.lower() + '%',))
        return self.cur.fetchall()
