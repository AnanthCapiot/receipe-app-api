from django.test import TestCase
from app.calc import add,subract


class CalcTest(TestCase):

    # -- all unit test functions should begin with test in lower case
    def test_add_numbers(self):
        """ Test addition of numbers here """
        self.assertEquals(add(3,8), 11)

    def test_subract_numbers(self):
        """ Values are subracted and asserted"""
        self.assertEquals(subract(5,7),6)