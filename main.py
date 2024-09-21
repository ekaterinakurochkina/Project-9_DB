import requests
import psycopg2
from src.db_manager import DBManager
# from src.utils import
from config import CONN

try:
    with CONN:
        with CONN.cursor() as cur:
            # работа с базой данных, вызовы команд в бд через курсор
            pass

finally:
    CONN.close()

def user_interaction():
    """Функция для взаимодействия с пользователем"""

    search_vacancy = input("Введите название вакансии для поиска: ")
    pages = int(input("Введите количество страниц с вакансиями для загрузки с сайта hh.ru: "))
    per_page = int(input("Введите количество вакансий на странице (не более 100): "))


# Создание экземпляра класса для работы с API сайта hh.ru
    hh_api = ApiWork()


#Получение вакансий с hh.ru в формате json и преобразование внутри метода в python-список словарей
    response = hh_api.get_response(search_vacancy, per_page)
    hh_vacancies = hh_api.get_vacancies(search_vacancy, pages)


# преобразование python-списка словарей в список экземпляров класса Vacancy
    vacancy_object_list = Vacancy.from_json_to_list(hh_vacancies)


# преобразование списка экземпляров класса Vacancy в список словарей python по необходимым ключам
    list_of_dicts = Vacancy.list_of_dicts(vacancy_object_list)


    print("Вакансии загружены с сайта hh.ru")

#Поиск по ключевому слову
    filter_word = input("Введите ключевое слово для его поиска в описании вакансии: ")
    print(f"Вакансии отфильтрованы по слову '{filter_word}' в описании.")

# Запись данных в файл json
    json_vacancy = ToJson(VACANCIES_PATH_JSON)
    print(json_vacancy)
    json_vacancy.add_data(list_of_dicts)
    print("Данные отсортированы по величине зарплаты.\n")

    top_n = int(input("Сколько вакансий с наибольшей зарплатой вывести на экран? Введите число: "))

# Вывод топ вакансий по зарплате
    top_sorted = sorted_data(filter_word, "salary", top_n)

# Удаление вакансии из списка
#     del_key = input("Если хотите удалить вакансию из файла, введите ее ID: ")

    delete_list = input("Если хотите удалить вакансии, очистив файл, введите 1: ")
    if delete_list == "1":
        data_delete = ToJson.del_data()
        print("Данные удалены из файла")
    print("Программа завершена")

if __name__ == "__main__":
    user_interaction()