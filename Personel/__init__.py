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
        self.__class__.employee_id += 1
        self.__class__.employees.append(self)
        self.employee_id = self.__class__.employee_id
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


def main():
    e1 = Employee("Гольцов Максим Алеексеевич", "+7-929-371-15-68", "mag25@tpu.ru")
    e2 = Employee("Калякулин Семён Олегович", "+7-929-371-90-26", "sok9@tpu.ru")

    c1 = Complaint("Гольцов Максим Алеексеевич", "Стажер БЕЗ стажа")
    c1 = Complaint("Гольцов Максим Алеексеевич", "Не пофиксил багу")

    print(e1.get_employee_id())
    print(e1.get_complaints())


if __name__ == '__main__':
    main()
