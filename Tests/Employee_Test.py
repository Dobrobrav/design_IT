import unittest
from Personel.__init__ import *


class EmployeeTest(unittest.TestCase):
    def test_get_name(self):
        e1 = Employee("Калякулин Семён Олегович", "+7-929-371-90-26", "sok9@tpu.ru")
        self.assertEqual(e1.get_name(), "Калякулин Семён Олегович")  # add assertion here

    def test_get_number(self):
        e2 = Employee("Калякулин Семён Олегович", "+7-929-371-90-26", "sok9@tpu.ru")
        self.assertEqual(e2.get_contact_number(), "+7-929-371-90-26")

    def test_get_email(self):
        e3 = Employee("Калякулин Семён Олегович", "+7-929-371-90-26", "sok9@tpu.ru")
        self.assertEqual(e3.get_email(), "sok9@tpu.ru")

    def test_get_complaints(self):
        e1 = Employee("Калякулин Семён Олегович", "+7-929-371-90-26", "sok9@tpu.ru")
        c1 = Complaint("Калякулин Семён Олегович", "Плохо работает")
        c2 = Complaint("Калякулин Семён Олегович", "Мало работает")
        self.assertEqual(e1.get_complaints(), f"Жалобы на {e1.get_name()}: Плохо работает; Мало работает")

    def test_wrong_name_type(self):
        with self.assertRaises(ValueError) as e:
            e1 = Employee(123, "+7-929-371-90-26", "sok9@tpu.ru")


if __name__ == '__main__':
    unittest.main()
