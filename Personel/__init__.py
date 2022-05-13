from typing import Any


class Employee:
    __employee_id: int = 0
    __name: str
    __contact_number: str
    __email: str
    __health_state: bool
    __faults: list
    __complaints: list
    __gratitudes: list
    __achievements: list[str]
    __employees: list = []

    def __init__(self, name: str, contact_number: str, email: str):
        Employee.__employee_id += 1
        Employee.__employees.append(self)
        self.__employee_id = Employee.__employee_id
        self.set_name(name)
        self.set_contact_number(contact_number)
        self.set_email(email)
        self.__complaints = []

    # def __del__(self):
    #     print(f"{self.name} больше здесь не работает")

    def set_id(self, employee_id: int):
        self.__employee_id = employee_id

    def set_contact_number(self, contact_number: str):
        if type(contact_number) is not str:
            raise ValueError("контактный телефон должен быть строкой")

        self.__contact_number = contact_number

    def set_email(self, email: str):
        if type(email) is not str:
            raise ValueError("email-адрес должен быть строкой")

        self.__email = email

    def set_name(self, name: str):
        if type(name) is not str:
            raise ValueError("имя должно быть строкой")

        self.__name = name

    def add_complaint(self, complaint):
        self.__complaints.append(complaint)

    def get_employee_id(self):
        return self.__employee_id

    def get_name(self):
        return self.__name

    def get_contact_number(self):
        return self.__contact_number

    def get_email(self):
        return self.__email

    def get_complaints(self):
        return f"Жалобы на {self.__name}: {'; '.join([complaint.text for complaint in self.__complaints])}"

    @classmethod
    def get_employee_by_name(cls, name):
        for employee in cls.__employees:
            if employee.__name == name:
                return employee

    @staticmethod
    def __print_smt(smt: str) -> None:
        print(smt)


class Complaint:
    employee_id: int
    employee_name: str
    employee: Employee
    text: str

    def __init__(self, name: str, text: str):
        self.employee_name = name
        self.text = text
        self.employee = Employee.get_employee_by_name(name)
        self.employee.add_complaint(self)
        self.employee_id = self.employee.get_employee_id()


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DataBase(metaclass=MetaSingleton):
    user: str
    password: str
    port: int
    # __instance: 'DataBase | None' = None
    #
    # def __new__(cls, *args, **kwargs):
    #     if cls.__instance is None:
    #         cls.__instance = super().__new__(cls)
    #
    #     return cls.__instance
    #
    # def __del__(self):
    #     DataBase.__instance = None

    def __init__(self, user, password, port):
        self.user = user
        self.password = password
        self.port = port

    def connect(self):
        print(f"Соединение с БД: {self.user}, {self.password}, {self.port}")

    def close(self):
        print("Закрытие соединения с БД")

    def read(self):
        print("Данные из БД")

    def write(self, data):
        print(f"Запись в БД: {self.data}")


if __name__ == '__main__':
    Employee._Employee__print_smt("abc")