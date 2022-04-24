import enum
import os
import random
import json

from pathlib import Path

with Path(os.getcwd()).joinpath("SkakovLabO4ka/words.json").open("r") as file:
    WORD_LIST = json.load(file)


class DataFlag(enum.Enum):
    INT = "int"
    FLOAT = "float"
    PHONEBOOK = "phonebook"


def generate_data(flag: DataFlag):
    n = random.randint(1, 20)
    lst = [generate_element(flag) for _ in range(n)]
    return lst


def generate_element(flag: DataFlag):
    if flag == DataFlag.INT:
        return random.randint(-2147483648, 2147483647)
    elif flag == DataFlag.FLOAT:
        return random.random()
    elif flag == DataFlag.PHONEBOOK:
        return (random.choice(WORD_LIST), random.choice(WORD_LIST),
                random.choice(WORD_LIST), random.randint(1, 10 ** 11 - 1))
    else:
        raise ValueError("flag should be either 0 or 1 or 2")

# add hints to every function in a file


def answer(data: list, is_reversed=False):
    return sorted(data, reverse = is_reversed)


