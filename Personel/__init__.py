from typing import Any, Type
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum


def main():
    flyweight_factory = FlyweightFactory()
    product_maker = ProductMaker(flyweight_factory)
    mediator = ProductAPI()

    print(f"Создано легковесов: {flyweight_factory.total}")
    print(f"Создано товаров: {product_maker.total}, \n")

    headphones = product_maker.make_product(mediator, "headphones", 10, picture="pic1")
    print(f"Создано легковесов: {flyweight_factory.total}")
    print(f"Создано товаров: {product_maker.total}, \n")

    tablet = product_maker.make_product(mediator, "tablet", 100, picture="pic1")
    print(f"Создано легковесов: {flyweight_factory.total}")
    print(f"Создано товаров: {product_maker.total}, \n")

    watch = product_maker.make_product(mediator, "watch", 50, picture="pic2")
    print(f"Создано легковесов: {flyweight_factory.total}")
    print(f"Создано товаров: {product_maker.total}, \n")

    # m1 = ProductAPI()
    # flyweight_factory = FlyweightFactory()
    # product_maker = ProductMaker(flyweight_factory)
    #
    # charger = product_maker.make_product(m1, "Charger", 10)
    #
    # samsung = Supplier(m1, "Samsung")
    # LG = Supplier(m1, "LG")
    # apple = Supplier(m1, "Apple")
    # xiaomi = Supplier(m1, "Xiaomi")
    #
    # for supplier, price in zip((samsung, LG, apple, xiaomi), (13.6, 11.9, 19.99, 3.99)):
    #     supplier.set_price(charger, price)
    #
    # print(m1.get_prices(charger))
    #
    # m1.set_strategy(PricesWithSellersStrategy)
    # print(m1.get_prices(charger))


class FeedbackType(Enum):
    complaint = 1
    gratitude = 2
    comment = 3
    suggestion = 4


class PricesShowingStrategy(ABC):
    """ Showing prices strategy interface """

    @staticmethod
    @abstractmethod
    def get_prices(mediator: 'ProductAPI',
                   proxy_product: 'IProduct') -> tuple[str, ...]:
        ...


class PricesWithSellersStrategy(PricesShowingStrategy):
    """ class of showing prices with the sellers strategy """

    @staticmethod
    def get_prices(mediator: 'ProductAPI',
                   proxy_product: 'ProxyProduct') -> tuple[str, ...]:
        return tuple(f"{supplier.get_name()}: {supplier.get_price(proxy_product)}$"
                     for supplier in mediator.get_suppliers()
                     if supplier.get_price(proxy_product))


class PricesOnlyStrategy(PricesShowingStrategy):
    """ class of only showing prices strategy """

    @staticmethod
    def get_prices(mediator: 'ProductAPI',
                   proxy_product: 'ProxyProduct') -> tuple[str, ...]:
        return tuple(f"{supplier.get_price(proxy_product)}$"
                     for supplier in mediator.get_suppliers()
                     if supplier.get_price(proxy_product))


class IProduct(ABC):
    """Interface for proxy"""

    @abstractmethod
    def get_id(self) -> int:
        """Interface method."""

    @abstractmethod
    def set_name(self, name: str) -> None:
        """Interface method."""

    @abstractmethod
    def get_name(self) -> str:
        """Interface method."""

    @abstractmethod
    def set_quantity(self, quantity: int) -> None:
        """Interface method."""

    @abstractmethod
    def get_quantity(self) -> int:
        """Interface method."""

    @abstractmethod
    def set_price(self, price: int | float) -> None:
        """Interface method."""

    @abstractmethod
    def get_price(self) -> float:
        """Interface method."""


class Product(IProduct):
    """Класс для работы с продуктами"""
    __id: list['Product'] = []
    __name: str
    __quantity: int
    __price: int | None = None
    __mediator: 'ProductAPI'
    _flyweight: 'ProductPictureFlyweight'

    def __init__(self, name: str, price: float, quantity: int,
                 flyweight: 'ProductPictureFlyweight'):
        self.__class__.__id.append(self)
        self.set_name(name)
        self.set_quantity(quantity)
        self.set_price(price)
        self._flyweight = flyweight

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


class ProxyProduct(IProduct):
    """Класс для работы с продуктами"""
    product: Product

    def __init__(self, mediator: 'ProductAPI', name: str, price: int | float,
                 quantity: int, flyweight: 'ProductPictureFlyweight'):
        if not (isinstance(mediator, ProductAPI) and isinstance(name, str)
                and isinstance(price, (int, float)) and isinstance(quantity, int)
                and isinstance(flyweight, ProductPictureFlyweight)):
            raise TypeError("Введенные данные не соответствуют требованиям по типу")

        self.product = Product(name, price, quantity, flyweight)
        self.__mediator = mediator
        mediator.add_product(self)

    def __str__(self) -> str:
        return f"ProxyProduct: '{self.product.get_name()}'"

    def get_id(self) -> int:
        return self.product.get_id()

    def set_name(self, name: str) -> None:
        if not isinstance(name, str):
            raise ValueError("name должно быть str")
        self.product.set_name(name)

    def get_name(self) -> str:
        return self.product.get_name()

    def set_quantity(self, quantity: int) -> None:
        if not isinstance(quantity, int):
            self.product.set_quantity(quantity)

    def get_quantity(self) -> int:
        return self.product.get_quantity()

    def set_price(self, price: int | float) -> None:
        if not isinstance(price, (int, float)):
            raise ValueError("price должен быть числом")
        self.product.set_price(price)

    def get_price(self) -> float:
        return self.product.get_price()


class ProductPictureFlyweight:
    """ Flyweight for pictures class """
    picture: str

    def __init__(self, picture: str):
        self.picture = picture

    def __repr__(self) -> str:
        return str(self.picture)


class FlyweightFactory:
    """ Flyweight factory class"""
    _flyweights: list[ProductPictureFlyweight]

    def __init__(self):
        self._flyweights = []

    def get_flyweight(self, picture: str) -> ProductPictureFlyweight:
        filtered_flyweights: list = list(filter(lambda x: x.picture == picture,
                                                self._flyweights))

        if filtered_flyweights:
            return filtered_flyweights[0]
        else:
            flyweight = ProductPictureFlyweight(picture)
            self._flyweights.append(flyweight)
            return flyweight

    @property
    def total(self):
        return len(self._flyweights)


class ProductMaker:
    """ Product factory class """
    _flyweight_factory: FlyweightFactory
    _products: list[IProduct]

    def __init__(self, flyweight_factory: FlyweightFactory):
        self._flyweight_factory = flyweight_factory
        self._products = []

    def make_product(self, mediator: 'ProductAPI', name: str, price: int | float,
                     quantity: int = 0,
                     picture: str = "default_picture") -> IProduct:
        flyweight = self._flyweight_factory.get_flyweight(picture)
        product = ProxyProduct(mediator, name, price, quantity, flyweight)
        self._products.append(product)

        return product

    @property
    def total(self):
        return len(self._products)


class Supplier:
    """Класс для работы с поставщиками"""
    __id: int = 0
    __name: str
    __prices: dict[IProduct, int]
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

    def set_price(self, proxy_product: IProduct, price: float) -> None:
        self.__prices[proxy_product] = int(price * 100)

    def get_price(self, proxy_product: ProxyProduct) -> float:
        return self.__prices[proxy_product] / 100


class Purchase:
    """Класс для работы с покупками"""
    __id: int = 0
    __number: int
    __products_quantity: dict[ProxyProduct, int]
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

    def get_products_quantity(self) -> dict[ProxyProduct, int]:
        return self.__products_quantity

    def add_product(self, proxy_product: ProxyProduct,
                    quantity: int = 1) -> None:
        for _ in range(quantity):
            if proxy_product in self.__products_quantity:
                self.__products_quantity[proxy_product] += 1
            else:
                self.__products_quantity[proxy_product] = 1

    def get_total(self) -> float:
        return sum(product.get_price() * quantity
                   for product, quantity in self.__products_quantity.items())


class ProductAPI:
    """Медиатор для связывания продуктов, поставщиков и покупок"""
    __suppliers: list[Supplier]
    __purchases: list[Purchase]
    __products: list[ProxyProduct]
    _strategy: Type[PricesShowingStrategy] = PricesOnlyStrategy

    def __init__(self):
        self.__products = []
        self.__purchases = []
        self.__suppliers = []

    def add_supplier(self, supplier: Supplier) -> None:
        self.__suppliers.append(supplier)

    def add_purchase(self, purchase: Purchase) -> None:
        self.__purchases.append(purchase)

    def add_product(self, proxy_product: ProxyProduct) -> None:
        self.__products.append(proxy_product)

    def get_suppliers(self) -> tuple[Supplier]:
        return tuple(self.__suppliers)

    def get_products(self) -> tuple[ProxyProduct]:
        return tuple(self.__products)

    def get_purchases(self) -> tuple[Purchase]:
        return tuple(self.__purchases)

    def set_strategy(self, strategy: Type[PricesShowingStrategy]):
        self._strategy = strategy

    def get_prices(self, proxy_product: IProduct) -> tuple[str, ...]:
        return self._strategy.get_prices(self, proxy_product)

    def get_purchases_with_product(self,
                                   product: Product) -> tuple[Purchase, ...]:
        return tuple(purchase for purchase in self.get_purchases()
                     if product in purchase.get_products_quantity())


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

    def __init__(self, name: str, contact_number: str = "some_number",
                 email: str = "some_email"):
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


class State(ABC):
    """Abstract class-state"""

    @staticmethod
    @abstractmethod
    def read(feedback: 'FeedBack'):
        ...

    @staticmethod
    @abstractmethod
    def is_read():
        ...


class Read(State):
    """class-state Read"""

    @staticmethod
    def read(feedback: 'FeedBack'):
        print(f"feedback '{feedback}' is already read")

    @staticmethod
    def is_read():
        return True


class Unread(State):
    """class-state Unread"""

    @staticmethod
    def read(feedback: 'FeedBack'):
        print(f"feedback '{feedback}' has been read")
        feedback.set_state(Read)

    @staticmethod
    def is_read():
        return False


class FeedBack(ABC):
    """Абстрактный класс для работы с фидбеком"""
    date_and_time: datetime
    customer_name: str
    contact_details: str
    text: str
    _state: Type[State]

    def __init__(self, text: str, customer_name: str, contact_details: str):
        self.date_and_time = datetime.now()
        self.customer_name = customer_name
        self.contact_details = contact_details
        self.text = text
        self._state = Unread

    def set_state(self, state: Type[State]):
        self._state = state

    def read(self):
        self._state.read(self)

    def is_read(self):
        return self._state.is_read()


class FeedbackToEmployee(FeedBack, ABC):
    """Класс для работы с жалобами"""
    employee_id: int
    employee_name: str  # Надо ли это хранить (думаю, что нет)
    employee: Employee

    def __init__(self, employee_name: str, text: str,
                 customer_name: str, contact_details: str):
        super().__init__(text, customer_name, contact_details)
        self.employee_name = employee_name
        self.employee = Employee.get_employee_by_name(employee_name)
        self.employee.add_complaint(self)
        self.employee_id = self.employee.get_employee_id()


class Gratitude(FeedbackToEmployee):
    """Класс для работы с благодарностями от посетителей."""

    def __init__(self, employee_name: str, text: str,
                 customer_name: str, contact_details: str):
        super().__init__(employee_name, text, customer_name, contact_details)
        self.set_employee_name(employee_name)

    def __str__(self):
        return f"Благодарность от {self.customer_name} для {self.employee_name}"

    def set_employee_name(self, employee_name: str) -> None:
        self.employee_name = employee_name


class Complaint(FeedbackToEmployee):
    """Класс для работы с благодарностями от посетителей."""

    def __init__(self, employee_name: str, text: str,
                 customer_name: str, contact_details: str = "some_contact"):
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


class FeedbackToEmployeeFactory(ABC):
    """Абстрактная фабрика фидбеков."""

    @abstractmethod
    def create_anonym_feedback(self, employee_name: str, text: str) -> FeedBack:
        """Абстрактный метод."""

    @abstractmethod
    def create_named_feedback(self, employee_name: str, text: str,
                              customer_name: str,
                              contact_details: str) -> FeedBack:
        """Абстрактный метод."""

    @staticmethod
    def create_feedback(feedback_type: FeedbackType, *args) -> FeedBack:
        """Фабричный метод для создания экземпляров класса Feedback."""

        factory_dict = {
            FeedbackType.complaint: Complaint,
            FeedbackType.gratitude: Gratitude,
            FeedbackType.suggestion: Suggestion,
            FeedbackType.comment: Comment,
        }
        return factory_dict[feedback_type](*args)


class GratitudeFactory(FeedbackToEmployeeFactory):
    """Фабрика отзывов и предложений"""

    def create_anonym_feedback(self, employee_name: str, text: str) -> FeedBack:
        return self.create_feedback(
            FeedbackType.gratitude, employee_name, text, "Anonym", "Anonym"
        )

    def create_named_feedback(self, employee_name: str, text: str,
                              customer_name: str,
                              contact_details: str) -> FeedBack:
        return self.create_feedback(FeedbackType.gratitude, employee_name,
                                    text, customer_name, contact_details)


class ComplaintFactory(FeedbackToEmployeeFactory):
    """Фабрика жалоб и благодарностей"""

    def create_anonym_feedback(self, employee_name: str, text: str) -> FeedBack:
        return self.create_feedback(
            FeedbackType.complaint, employee_name, text, "Anonym", "Anonym"
        )

    def create_named_feedback(self, employee_name: str, text: str,
                              customer_name: str,
                              contact_details: str) -> FeedBack:
        return self.create_feedback(FeedbackType.complaint, employee_name,
                                    text, customer_name, contact_details)


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

    def __init__(self, user: str = "default_user",
                 password: str = "default_password", port: int = "default_port"):
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
