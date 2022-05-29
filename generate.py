"""This class is responsible for providing random data for test cases and solving"""
import random

def generate_data(length: int):
    """Generates list of given data type and size equal to length"""
    lst = [generate_element(3, 3), "+", generate_element(3, 3)]
    return lst

"""
#ToDo:
create
context-free grammar that allows only certain symbols:
+, -, *, /, ~, %, <, <=, >, >=, ==, !=, _
"""

def generate_element(min_digits: int, max_digits: int) -> int:
    """Generates and returns an element in range [-10**mindigits, 10**max_digits]"""
    return random.randint(-10**min_digits, 10**max_digits)

def answer(data: list, is_reversed: bool = False):
    return sorted(data, reverse=is_reversed)
