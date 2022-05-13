from typing import Any


class Employee:
    employee_id: int = 0
    name: str
    contact_number: str
    email: str
    health_state: bool
    faults: list
    complaints: list
    gratitudes: list
    achievements: list[str]
    employees: list = []

    def __init__(self, name: str, contact_number: str, email: str):
        Employee.employee_id += 1
        Employee.employees.append(self)
        self.employee_id = Employee.employee_id
        self.name = name
        self.contact_number = contact_number
        self.email = email
        self.complaints = []

    # def __del__(self):
    #     print(f"{self.name} больше здесь не работает")

    def set_id(self, employee_id: int):
        self.employee_id = employee_id

    def set_contact_number(self, contact_number: str):
        self.contact_number = contact_number

    def set_email(self, email: str):
        self.email = email

    def set_name(self, name: str):
        self.name = name

    def add_complaint(self, complaint):
        self.complaints.append(complaint)

    def get_employee_id(self):
        return self.employee_id

    def get_name(self):
        return self.name

    def get_contact_number(self):
        return self.contact_number

    def get_email(self):
        return self.email

    def get_complaints(self):
        return f"Жалобы на {self.name}: {'; '.join([complaint.text for complaint in self.complaints])}"

    @classmethod
    def get_employee_by_name(cls, name):
        for employee in cls.employees:
            if employee.name == name:
                return employee


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


def main():
    # e1 = Employee("Гольцов Максим Алеексеевич", "+7-929-371-15-68", "mag25@tpu.ru")
    # e2 = Employee("Калякулин Семён Олегович", "+7-929-371-90-26", "sok9@tpu.ru")
    #
    # c1 = Complaint("Гольцов Максим Алеексеевич", "Стажер БЕЗ стажа")
    # c1 = Complaint("Гольцов Максим Алеексеевич", "Не пофиксил багу")
    #
    # print(e1.get_employee_id())
    # print(e1.get_complaints())

    db1 = DataBase("user", "qwerty", 123)
    db2 = DataBase("admin", "qwerty123", 456)
    print(db1.user, db1.password, db1.port)
    print(db2.user, db2.password, db2.port)



if __name__ == '__main__':
    main()
