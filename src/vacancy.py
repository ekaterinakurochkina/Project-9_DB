class Vacancy:
    """Класс для работы с вакансиями, содержащий методы сравнения данных по вакансиям,
    а также по валидации этих данных"""

    __slots__ = ("id", "name", "salary", "alternate_url", "requirement")

    def __init__(self, id, name, salary, alternate_url, requirement):
        # перед присвоением данных проводим их валидацию
        self.id = self.__validate_id(id)
        self.name = self.__validate_name(name)
        self.salary = self.__validate_salary(salary)
        self.alternate_url = self.__validate_url(alternate_url)
        self.requirement = self.__validate_requirement(requirement)

    def __str__(self):
        """Строковое представление вакансии"""
        return f"ID вакансии:{self.id}, Наименование: {self.name}, Зарплата: {self.salary}, Url вакансии: {self.alternate_url}, Требования к соискателю: {self.requirement}"

    def __lt__(self, other) -> bool:
        """Метод сравнения от большего к меньшему"""
        if isinstance(other, Vacancy):
            return self.salary < other.salary
        return NotImplemented

    # Приватные методы для валидации данных
    def __validate_id(self, id):
        if not isinstance(id, str) or not id.isdigit():
            raise ValueError("Ошибка id вакансии")
        return id

    def __validate_name(self, name):
        if not isinstance(name, str) or not name:
            raise ValueError("Ошибка имени вакансии")
        return name

    def __validate_salary(self, salary):
        if salary is None:
            return 0
        elif not isinstance(salary, (int, float)):  # or salary < 0:
            raise ValueError("Ошибка значения зарплаты вакансии")
        return salary

    def __validate_url(self, alternate_url):
        if not isinstance(alternate_url, str) or not alternate_url.startswith("http"):
            raise ValueError("Ошибка url адреса вакансии")
        return alternate_url

    def __validate_requirement(self, requirement):
        if requirement != None and not isinstance(requirement, str):
            raise ValueError("Ошибка требований к претенденту")
        elif requirement == None:
            return "Требования к соискателю отсутствуют."
        return requirement

    @staticmethod
    def salary_data(vacancy):
        """Метод, возвращающий зарплату, независимо от того, представлена ли она диапазоном"""
        if vacancy["salary"] is None:
            salary = 0
            return salary
        elif vacancy["salary"]["from"] and vacancy["salary"]["to"] is None:
            salary = vacancy["salary"]["from"]
            return salary
        elif vacancy["salary"]["from"] is None and vacancy["salary"]["to"]:
            salary = vacancy["salary"]["to"]
            return salary
        else:
            salary = vacancy["salary"]["from"]
            return salary

    def to_dict(vacancy):
        """Метод, возвращающий вакансию в виде словаря"""
        vacancy_dict = {
            "id": vacancy.id,
            "name": vacancy.name,
            "salary": vacancy.salary,
            "alternate_url": vacancy.alternate_url,
            "requirement": vacancy.requirement,
        }
        return vacancy_dict

    def list_of_dicts(vacancy_list):
        """метод, создающий список словарей вакансий"""
        list_of_dicts = []
        for vacancy in vacancy_list:
            list_of_dicts.append(vacancy.to_dict())
        return list_of_dicts
