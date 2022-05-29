from collections import namedtuple
from math import sqrt

Operation = namedtuple("Operation", ["arity", "oper"])

table = {
    "+" : Operation(2, lambda x, y: x + y),
    "-" : Operation(2, lambda x, y: x - y),
    "*" : Operation(2, lambda x, y: x * y),
    "/" : Operation(2, lambda x, y: x // y),
    
    "~" : Operation(1, lambda x: int(sqrt(x))),
    "%" : Operation(1, lambda x, y: x % y),
    "_" : Operation(1, lambda x: -x),

    # not clear
    "<" : None,
    "<=": None,
    ">" : None,
    ">=": None,
    "==": None,
    "!=": None,
}
