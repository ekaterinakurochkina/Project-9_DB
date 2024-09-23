import requests


class ApiWork:
    """Класс для получения вакансий через API"""

    def __init__(self):
        self.__url = None
        self.__params = None

    def get_response(self):
        """Отправляем запрос по API"""
        response = requests.get(
            self.__url, params=self.__params
        )
        if response.status_code == 200:
            return response.json()["items"]
        else:
            raise Exception(
                f"Запрос не был успешным. Возможная причина: {response.reason}"
            )
    def get_employers(self):
        """Получаем 10 работодателей, у которых есть открытые вакансии"""
        self.__url = "https://api.hh.ru/employers"
        self.__params = {
            "sort_by": "by_vacancies_open",
            "per_page": 10
        }
        return self.get_response()


    def get_vacancies(self, employer_id):
        """Получаем 50 вакансий у заданного работодателя"""

        self.__url = "https://api.hh.ru/vacancies"
        self.__params = {
            "employer_id": employer_id,
            "per_page": 50
        }
        return self.get_response()

