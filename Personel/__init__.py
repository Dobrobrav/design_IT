from typing import Any
from abc import ABC, abstractmethod


def main():
    m1 = ProductAPI()
    apple = Product(m1, "apple")
    pineapple = Product(m1, "pineapple")

    s1 = Supplier(m1, "supplier_name")
    s2 = Supplier(m1, "supplier_name")
    s3 = Supplier(m1, "supplier_name")

    s1.set_price(apple, 500.25)
    s2.set_price(apple, 334.75)
    s3.set_price(apple, 450)

    print(m1.get_prices(apple))


class Product:
    """Класс для работы с продуктами"""
    __id: int = 0
    __name: str
    __quantity: int
    __price: int
    __mediator: 'ProductAPI'

    def __init__(self, mediator: 'ProductAPI', name: str, quantity: int = 0):
        Product.__id += 1
        self.id = Product.__id
        self.set_name(name)
        self.set_quantity(quantity)
        self.__mediator = mediator
        mediator.add_product(self)

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

    def set_name(self, name: str) -> None:
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def set_price(self, product: Product, price: float) -> None:
        self.__prices[product] = int(price * 100)

    def get_price(self, product: Product) -> float:
        return self.__prices[product] / 100


class Purchase:
    """Класс для работы с поставщиками"""
    __id: int = 0
    __number: int
    __products_quantity: dict[Product, int]
    __mediator: 'ProductAPI'

    def __init__(self, number: int, mediator: 'ProductAPI'):
        Purchase.__id += 1
        self.__id = Purchase.__id
        self.set_number(number)
        self.__mediator = mediator
        mediator.add_purchase(self)

    def set_number(self, number: int) -> None:
        self.__number = number


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


class SupplierAPI:
    """Медиатор для связывания продуктов, поставщиков и покупок"""
    __products: list[Product]
    # __suppliers: list['Supplier']
    __purchases: list['Purchase']

    def __init__(self):  # Надо создать три дочерних класса и в каждом из них в ините прописать то, что нужно
        self.__products = []
        # self.__suppliers = []
        self.__purchases = []

    def add_product(self, product: Product) -> None:
        self.__products.append(product)

    # def add_supplier(self, supplier: str) -> None:
    #     self.__suppliers.append(supplier)

    def add_purchase(self, purchase: 'Purchase') -> None:
        self.__purchases.append(purchase)


class PurchaseAPI:
    """Медиатор для связывания продуктов, поставщиков и покупок"""
    __products: list[Product]
    __suppliers: list['Supplier']

    # __purchases: list['Purchase']

    def __init__(self):  # Надо создать три дочерних класса и в каждом из них в ините прописать то, что нужно
        self.__products = []
        # self.__suppliers = []
        self.__purchases = []

    def add_product(self, product: Product) -> None:
        self.__products.append(product)

    def add_supplier(self, supplier: str) -> None:
        self.__suppliers.append(supplier)

    # def add_purchase(self, purchase: 'Purchase') -> None:
    #     self.__purchases.append(purchase)


class Employee:
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

    def __init__(self, name: str, contact_number: str, email: str):
        Employee.__id += 1
        Employee.__employees.append(self)
        self.__id = Employee.__id
        self.set_name(name)
        self.set_contact_number(contact_number)
        self.set_email(email)
        self.__complaints = []

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
    _instances: dict['MetaSingleton', Any] = {}

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
