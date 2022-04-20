import enum
import os
import random
import json
from pathlib import Path


with Path(os.getcwd()).joinpath("words.json").open("r") as file:
    WORD_LIST = json.load(file)

class DataFlag(enum.Enum):
    INT = 0
    FLOAT = 1
    PHONEBOOK = 2


def generate_data(flag):
    n = random.randint(1, 20)
    lst = [generate_element(flag) for _ in range(n)]
    return lst


def generate_element(flag):
    # make for python3.7
    match flag:
        case DataFlag.INT: return random.randint(-2147483648, 2147483647)
        case DataFlag.FLOAT: return random.random()
        case DataFlag.PHONEBOOK: return (random.choice(WORD_LIST), random.choice(WORD_LIST),
                                         random.choice(WORD_LIST), random.randint(1, 10 ** 11 - 1))
        case _: raise ValueError("flag should be either 0 or 1 or 2")


def answer(data, reversed=False):
    return sorted(data, reverse=reversed)
