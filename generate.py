"""
This class is responsible for providing random data for test cases and solving

cf grammar transitions
1 -> 1 1 +
1 -> 1 1 -
1 -> 1 1 /
1 -> 1 1 %

1 -> 1 ~
1 -> 1 _

1 -> number
"""

from collections import namedtuple, deque
from time import time
from collections import namedtuple
import random
from math import sqrt


Operation = namedtuple("Operation", ["arity", "oper"])
class NaN(int):
    def __ne__(self, __o: object) -> bool:
        return True

    def __eq__(self, __o: object) -> bool:
        return False
    
    def __ge__(self, __x: int) -> bool:
        return False

    def __le__(self, __x: int) -> bool:
        return False
    
    def __lt__(self, __x: int) -> bool:
        return False

    def __gt__(self, __x: int) -> bool:
        return False

    def __str__(self) -> str:
        return "NaN"

def factory(x, y, func):
    return NaN() if type(x) == NaN or type(y) == NaN else func(x, y)

table = {
    "+": Operation(2, lambda x, y: x + y),
    "-": Operation(2, lambda x, y: x - y),
    "*": Operation(2, lambda x, y: x * y),
    "/": Operation(2, lambda x, y: x // y),
    "%": Operation(2, lambda x, y: x % y),

    "~": Operation(1, lambda x: int(sqrt(x))),
    "_": Operation(1, lambda x: -x),

    "<":  Operation(2, lambda x, y: int(x < y)),
    "<=": Operation(2, lambda x, y: int(x <= y)),
    ">":  Operation(2, lambda x, y: int(x > y)),
    ">=": Operation(2, lambda x, y: int(x >= y)),
    "==": Operation(2, lambda x, y: int(x == y)),
    "!=": Operation(2, lambda x, y: int(x != y)),
}


def cf_grammar_transition(lst: list) -> list:
    """Generates new expression from the given"""
    new_lst = []
    one_cnt = 1
    for x in lst:
        if x == 1 and random.random() < 1 / 2:
            new_oper = random.choice(list(table.keys()))
            arity = table[new_oper].arity
            one_cnt += arity

            if arity == 1:
                new_lst.extend([1, new_oper])
            else:
                new_lst.extend([1, 1, new_oper])
        else:
            new_lst.append(x)
    return new_lst


def generate_data(n: int, min_digits: int = 2, max_digits: int = 2) -> list:
    """
    Generates expression with sz elements, where sz is approximately n <= sz < n * 2,
    and every numbers belongs lies within range [10**min_digits, 10**max_digits]
    """
    lst = [1]
    while len(lst) < n:
        lst = cf_grammar_transition(lst)
    for i, x in enumerate(lst):
        if x == 1:
            lst[i] = generate_element(min_digits, max_digits)
    return lst


def generate_element(min_digits: int, max_digits: int) -> int:
    """Generates and returns an element in range [-10**mindigits, 10**max_digits]"""
    return random.randint(-10 ** min_digits, 10 ** max_digits)


def solve(lst: list) -> int:
    stack = deque()
    for x in lst:
        if type(x) == str:
            arity, oper = table[x]
            tmp = []
            for _ in range(arity):
                tmp.append(stack.pop())
            try:
                stack.append(oper(*reversed(tmp)))
            except (ValueError, ZeroDivisionError):
                stack.append(NaN()) 
        else:
            stack.append(x)
    return list(stack)
