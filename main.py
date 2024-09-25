import requests
import psycopg2
from src.db_manager import DBManager
# from src.utils import
from src.utils import create_database, insert_data_to_database
from src.db_manager import DBManager
from src.api_access import ApiWork

from dotenv import load_dotenv
from src.utils import create_database, create_tables, insert_data_to_database
from src.db_manager import DBManager


def user_interaction():
    """Функция для взаимодействия с пользователем"""

    database_name = "db_hh"
    create_database("db_hh")
    create_tables("db_hh")
    insert_data_to_database("db_hh")

    db_manager = DBManager(database_name)

    print("\nДобрый день!")
    
    while True:
        print("""Предлагаем ознакомиться с вакансиями, представленными на сайте hh.ru
            Пожалуйста, выберите, какую информацию о десяти работодателях их вакансиях Вы хотите узнать:
            1. Список компаний и количество вакансий у каждой компании
            2. Список вакансий с указанием названия компании, зарплаты и ссылки на вакансию
            3. Средняя зарплата по вакансиям
            4. Список вакансий, у которых зарплата выше средней по всем вакансиям
            5. Список всех вакансий, в названии которых содержится ключевое слово
            6. Завершить работу программы
            """)
        user_choice = input("Ваш выбор: ")
        if user_choice == "1":
            list_employer = db_manager.get_companies_and_vacancies_count()
            print("Список всех компаний и количество вакансий у каждой компании:")
            for i in list_employer:
                print(i)
        elif user_choice == "2":
            list_vacancy_full = db_manager.get_all_employers()
            print("Список вакансий с указанием ID вакансии,названия вакансии, зарплаты минимальной и максимальной, ссылки на вакансию:")
            for i in list_vacancy_full:
                print(i)
        elif user_choice == "3":
            list_vacancy_avg_salary = db_manager.get_avg_salary()
            print("Список всех вакансий co средней зарплатой по вакансиям:")
            for i in list_vacancy_avg_salary:
                print(i)
        elif user_choice == "4":
            list_vacancy_avg_salary = db_manager.get_vacancies_with_higher_salary()
            print("Список всех вакансий с зарплатой выше средней:")
            for i in list_vacancy_avg_salary:
                print(i)
        elif user_choice == "5":
            keyword = input("Введите слово, по которому хотите отфильтровать вакансии: \n").lower()
            list_vacancy_keyword = db_manager.get_vacancies_with_keyword(keyword)
            print("Список всех вакансий в названии которых содержатся переданные в метод слова:")
            for i in list_vacancy_keyword:
                print(i)
        elif user_choice == "6":
            print("Работа программы завершена")
            break
        else:
            print("Работа программы завершена")
            break


if __name__ == "__main__":
    user_interaction()

