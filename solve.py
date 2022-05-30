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
            stack.append(oper(*reversed(tmp)))
        else:
            stack.append(x)
    return stack.pop()