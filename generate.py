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

from collections import namedtuple
import random
from math import sqrt
from collect import ValidCase


def generate_case(sz: int = 50):
    return ValidCase(generate_data(sz))

Operation = namedtuple("Operation", ["arity", "oper"])

table = {
    "+": Operation(2, lambda x, y: x + y),
    "-": Operation(2, lambda x, y: x - y),
    "*": Operation(2, lambda x, y: x * y),
    "/": Operation(2, lambda x, y: x // y),
    "%": Operation(2, lambda x, y: x % y),

    "~": Operation(1, lambda x: int(sqrt(x))),
    "_": Operation(1, lambda x: -x),

    # not clear
    # "<" : None,
    # "<=": None,
    # ">" : None,
    # ">=": None,
    # "==": None,
    # "!=": None,
}


def convert_data_to_string(data) -> str:
    """data - list from function generated data"""
    out = ''
    for i in data:
        if type(i) is int:
            for j in str(int):
                if j == '-':
                    out += '-'
                else:
                    out += j + '\n'
        else:
            out += i

    return out + '==\n'


def cf_grammar_transition(lst: list[int | str]) -> list[int | str]:
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


def generate_data(n: int, min_digits: int = 5, max_digits: int = 5) -> list[int | str]:
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
    return random.randint(0, 10 ** max_digits)

from collections import namedtuple, deque
from math import sqrt
from time import time

Operation = namedtuple("Operation", ["arity", "oper"])

table = {
    "+" : Operation(2, lambda x, y: x + y),
    "-" : Operation(2, lambda x, y: x - y),
    "*" : Operation(2, lambda x, y: x * y),
    "/" : Operation(2, lambda x, y: x // y),
    "%" : Operation(2, lambda x, y: x % y),
    
    "~" : Operation(1, lambda x: int(sqrt(x))),
    "_" : Operation(1, lambda x: -x),

    # not clear
    # "<" : None,
    # "<=": None,
    # ">" : None,
    # ">=": None,
    # "==": None,
    # "!=": None,
}

# the technical requirement is not clear, therefore solve return just int and not list[int]

def solve(lst: list[int | str]) -> int:
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
                return None
        else:
            stack.append(x)
    return list(stack)
