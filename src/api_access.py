import requests
from abc import ABC, abstractmethod
import os

# api_key = os.getenv("API_KEY")


class ApiAccess(ABC):
    """Абстрактный класс для работы с вакансиями по API"""

    @abstractmethod
    def get_response(self, keyword: str, per_page: int):
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str, per_page: int):
        pass


class ApiWork(ApiAccess):
    """Класс для получения вакансий через API"""

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User_Agent"}
        self.__params = {
            "text": "",
            "page": 0,
            "per_page": 100,
            "only_whith_salary": True,
        }
        self.__vacancies = []

    # page - номер страницы, 	Default: 0
    # per_page - количество элементов на странице, Default: 10
    # text - переданное значение ищется в полях вакансии, указанных в параметре search_field
    # only_with_salary - Показывать вакансии только с указанием зарплаты. По умолчанию false
    # order_by - Сортировка списка вакансий.

    def get_response(self, keyword, per_page):
        """Отправляем запрос по API"""
        self.__params["text"] = keyword
        self.__params["per_page"] = per_page
        response = requests.get(
            self.__url, headers=self.__headers, params=self.__params
        )
        if response.status_code == 200:
            return response
        else:
            raise Exception(
                f"Запрос не был успешным. Возможная причина: {response.reason}"
            )

    def get_vacancies(self, keyword: str, page: int):
        """Получаем вакансии"""

        try:
            while self.__params.get("page") < page:
                # response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                vacancies = self.get_response(keyword, page).json()[
                    "items"
                ]  # преобразуем ответ от API (в формате JSON) в Python-объект (список словарей)
                if not vacancies:
                    break
                self.__vacancies.extend(
                    vacancies
                )  # добавляем новые вакансии в уже существующий список вакансий
                self.__params["page"] += 1
                result_get_vacancies = self.__vacancies
            # print(result_get_vacancies)
            # print(type(result_get_vacancies))
            return result_get_vacancies
        except requests.exceptions.RequestException as e:
            # Обрабатываем ошибку при получении вакансий
            print(f"Ошибка API-запроса при получении вакансий: {e}")
            return []
# _______________

def get_hh_data(employer_ids):
    employer_ids = [4219, 78638, 198614, 774144, 5667343, 5919632, 6062708, 9301808, 9694561, 10571093]
    data = []
    for employer in employer_ids:
        employer_data =