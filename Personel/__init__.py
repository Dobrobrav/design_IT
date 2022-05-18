from typing import Any
from abc import ABC
from datetime import datetime
from enum import Enum


def main():
    db = DataBase()

    e1 = Employee("Гольцов")
    f1 = create_feedback(FeedbackType.complaint, "Гольцов", "Стажер без стажа", "Петров")
    print(f1.__dict__)


class FeedbackType(Enum):
    complaint = 1
    gratitude = 2
    comment = 3
    suggestion = 4


class Product:
    """Класс для работы с продуктами"""
    __id: list['Product'] = []
    __name: str
    __quantity: int
    __price: int | None = None
    __mediator: 'ProductAPI'

    def __init__(self, mediator: 'ProductAPI', name: str, price: float, quantity: int = 0):
        self.__class__.__id.append(self)
        self.set_name(name)
        self.set_quantity(quantity)
        self.__mediator = mediator
        self.set_price(price)
        mediator.add_product(self)

    def __del__(self):
        print(Product.__id)
        self.__class__.__id.remove(self)
        print(Product.__id)

    def __str__(self) -> str:
        return f"Product: '{self.get_name()}'"

    def get_id(self) -> int:
        return self.__class__.__id.index(self) + 1

    def set_name(self, name: str) -> None:
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def set_quantity(self, quantity: int) -> None:
        self.__quantity = quantity

    def get_quantity(self) -> int:
        return self.__quantity

    def set_price(self, price: int | float) -> None:
        if type(price) in (int, float):
            self.__price = int(price * 100)

    def get_price(self) -> float:
        return self.__price // 100


class Supplier:
    """Класс для работы с поставщиками"""
    __id: int = 0
    __name: str
    __prices: dict[Product, int]
    __mediator: 'ProductAPI'

    def __init__(self, mediator: 'ProductAPI', name: str):
        Supplier.__id += 1
        self.__id = Supplier.__id
        self.set_name(name)
        self.__prices = {}
        self.__mediator = mediator
        mediator.add_supplier(self)

    def __str__(self) -> str:
        return f"Supplier: '{self.get_name()}'"

    def set_name(self, name: str) -> None:
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def set_price(self, product: Product, price: float) -> None:
        self.__prices[product] = int(price * 100)

    def get_price(self, product: Product) -> float:
        return self.__prices[product] / 100


class Purchase:
    """Класс для работы с покупками"""
    __id: int = 0
    __number: int
    __products_quantity: dict[Product, int]
    __mediator: 'ProductAPI'

    def __init__(self, mediator: 'ProductAPI', number: int):
        Purchase.__id += 1
        self.__id = Purchase.__id
        self.set_number(number)
        self.__products_quantity = {}
        self.__mediator = mediator
        mediator.add_purchase(self)

    def __str__(self) -> str:
        return f"Purchase number: '{self.get_number()}'"

    def set_number(self, number: int) -> None:
        self.__number = number

    def get_number(self) -> int:
        return self.__number

    def get_products_quantity(self) -> dict[Product, int]:
        return self.__products_quantity

    def add_product(self, product: Product, quantity: int = 1) -> None:
        for _ in range(quantity):
            if product in self.__products_quantity:
                self.__products_quantity[product] += 1
            else:
                self.__products_quantity[product] = 1

    def get_total(self) -> float:
        return sum(product.get_price() * quantity for product, quantity in self.__products_quantity.items())


class ProductAPI:
    """Медиатор для связывания продуктов, поставщиков и покупок"""
    __suppliers: list[Supplier]
    __purchases: list[Purchase]
    __products: list[Product]

    def __init__(self):
        self.__products = []
        self.__purchases = []
        self.__suppliers = []

    def add_supplier(self, supplier: Supplier) -> None:
        self.__suppliers.append(supplier)

    def add_purchase(self, purchase: Purchase) -> None:
        self.__purchases.append(purchase)

    def add_product(self, product: Product) -> None:
        self.__products.append(product)

    def get_suppliers(self) -> tuple[Supplier]:
        return tuple(self.__suppliers)

    def get_products(self) -> tuple[Product]:
        return tuple(self.__products)

    def get_purchases(self) -> tuple[Purchase]:
        return tuple(self.__purchases)

    def get_prices(self, product: Product) -> tuple[float, ...]:
        return tuple(supplier.get_price(product) for supplier in self.__suppliers if supplier.get_price(product))

    def get_purchases_with_product(self, product: Product) -> tuple[Purchase, ...]:
        return tuple(purchase for purchase in self.get_purchases() if product in purchase.get_products_quantity())


class Employee:
    """Класс для работы с работниками магазина"""
    __id: int = 0
    __name: str
    __contact_number: str
    __email: str
    __health_state: bool
    __faults: list
    __complaints: list
    __gratitudes: list
    __achievements: list[str]
    __employees: list = []

    def __init__(self, name: str, contact_number: str = "some_number", email: str = "some_email"):
        Employee.__id += 1
        Employee.__employees.append(self)
        self.__id = Employee.__id
        self.set_name(name)
        self.set_contact_number(contact_number)
        self.set_email(email)
        self.__complaints = []

    def __str__(self):
        return f"Работник: {self.get_name()}"

    # def __del__(self):
    #     print(f"{self.name} больше здесь не работает")

    def set_id(self, employee_id: int):
        self.__id = employee_id

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
        return self.__id

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
            # print(f"{employee.get_name()}, {name}")
            if employee.get_name() == name:
                # print("found employee")
                return employee

    @staticmethod
    def __print_smt(smt: str) -> None:
        print(smt)


class FeedBack(ABC):
    """Абстрактный класс для работы с фидбеком"""
    date_and_time: datetime
    customer_name: str
    contact_details: str
    text: str

    def __init__(self, text: str, customer_name: str, contact_details: str):
        self.date_and_time = datetime.now()
        self.customer_name = customer_name
        self.contact_details = contact_details
        self.text = text


class FeedbackToEmployee(FeedBack):
    """Класс для работы с жалобами"""
    employee_id: int
    employee_name: str  # Надо ли это хранить (думаю, что нет)
    employee: Employee

    def __init__(self, employee_name: str, text: str, customer_name: str, contact_details: str):
        super().__init__(text, customer_name, contact_details)
        self.employee_name = employee_name
        self.employee = Employee.get_employee_by_name(employee_name)
        self.employee.add_complaint(self)
        self.employee_id = self.employee.get_employee_id()


class Gratitude(FeedbackToEmployee):
    """Класс для работы с благодарностями от посетителей."""
    def __init__(self, employee_name: str, text: str, customer_name: str, contact_details: str):
        super().__init__(employee_name, text, customer_name, contact_details)
        self.set_employee_name(employee_name)

    def __str__(self):
        return f"Благодарность от {self.customer_name} для {self.employee_name}"

    def set_employee_name(self, employee_name: str) -> None:
        self.employee_name = employee_name


class Complaint(FeedbackToEmployee):
    """Класс для работы с благодарностями от посетителей."""
    def __init__(self, employee_name: str, text: str, customer_name: str, contact_details: str = "some_contact"):
        super().__init__(employee_name, text, customer_name, contact_details)
        self.set_employee_name(employee_name)

    def __str__(self):
        return f"Жалоба от {self.customer_name} на {self.employee_name}"

    def set_employee_name(self, employee_name: str) -> None:
        self.employee_name = employee_name


class Comment(FeedBack):
    """Класс для работы с жалобами"""

    def __init__(self, text: str, customer_name: str,
                 contact_details: str = "some_contact"):
        super().__init__(text, customer_name, contact_details)


class Suggestion(FeedBack):
    """Класс для работы с жалобами"""

    def __init__(self, text: str, customer_name: str,
                 contact_details: str = "some_contact"):
        super().__init__(text, customer_name, contact_details)


def create_feedback(feedback_type: FeedbackType, *args) -> FeedBack:
    """Фабричный метод для создания экземпляров класса Feedback."""

    factory_dict = {
        FeedbackType.complaint: Complaint,
        FeedbackType.gratitude: Gratitude,
        FeedbackType.suggestion: Suggestion,
        FeedbackType.comment: Comment,
    }
    return factory_dict[feedback_type](*args)


class MetaSingleton(type):
    """Метакласс для реализации singleton"""
    _instances: dict['MetaSingleton', Any] = {}

    def __call__(cls, *args, **kwargs):
        print(cls)
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class DataBase(metaclass=MetaSingleton):
    """Класс для коннекта с БД"""
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

    def __init__(self, user: str = "default_user", password: str = "default_password", port: int = "default_port"):
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
        print(f"Запись в БД: {data}")


if __name__ == '__main__':
    main()
