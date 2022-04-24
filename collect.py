from __future__ import annotations
from generate import generate_data, DataFlag, answer
import os
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from solve import solve
import color_log

main_name = "Тест 3-его дз"
stop_after = 2

"""
Special classes
"""
working_directory = Path(os.getcwd())
program_name: Path
current_error = 0


class StopExc(Exception):
    pass


class TrueExc(Exception):
    pass


class ErrorExc(Exception):
    pass


class Case:
    def __init__(self, data: list[int | float | tuple[str, str, int]], is_reversed: bool, type: DataFlag):
        self.data = data
        self.is_reversed = is_reversed
        self.out = answer(data, is_reversed)
        self.type = type

    def __repr__(self):
        if self.type == DataFlag.PHONEBOOK:
            string = "\n".join(map(lambda x: " ".join(map(str, x)), self.data))
        else:
            string = "\n".join(map(str, self.data))

        return  f"{self.type.value}\n" \
                f"{'ascending' if self.is_reversed else 'descending'}\n" \
                f"{len(self.data)}\n" \
                f"{string}"

class Group(ABC):
    """
    This structure is superclass.
    There collect groups and cases.
    And run cases.
    """

    @property
    @abstractmethod
    def name(self):
        """
        This method should return information about the group.
        """
        pass

    def __init__(self, level=0):
        self.entities = []
        self.return_code = 0
        self.level = level

    @abstractmethod
    def _run_case(self, case: Case, inp: Path, out: Path):
        """
        This method should start and check one case, without unexpected exceptions.
        """
        pass

    @abstractmethod
    def load(self):
        """
        This method should add entities(cases or groups) in self.entities.
        """
        pass

    def run(self):
        """
        This method:

        1. Create input.txt output.txt, don't write.
        2. Call _run().
        3. Catch exceptions and wrong answerss. After 'stop_after' failed test will be stopped.
        """
        global current_error
        print(" " * self.level + self.name)
        for ent in self.entities:
            if issubclass(type(ent), Case):
                inp = working_directory.joinpath(f"inp{current_error}.txt")
                out = working_directory.joinpath(f"out{current_error}.txt")
                try:
                    self._run_case(ent, inp, out)
                except ErrorExc:
                    print(color_log.RED(f"Wrong. Test is saved in {inp} / {out}"))
                    current_error += 1
                    if current_error == stop_after:
                        exit()

            elif issubclass(ent, Group):
                _ent = ent(level = self.level + 1)
                _ent.load()
                _ent.run()


class MainGroup(Group):
    @property
    def name(self):
        return main_name

    def _run_case(self, case: Case, inp: Path, out: Path):
        raise "MainGroup doesn't run cases."

    def load(self):
        raise "MainGroup has no load method."


main_group = MainGroup()


def is_main_group(group_class):
    if not issubclass(group_class, Group):
        raise "is_test_group is a decorator for classes, that inherits from Group."
    main_group.entities.append(group_class)


"""
Personal classes
"""

class ValidGroup(Group, ABC):
    def _run_case(self, case: Case, inp: Path, out: Path):
        
        with open(inp, "w") as inp_f:
            inp_f.write(str(case))

        subprocess.call([program_name, str(inp), str(out)])
        if case.out == solve(out, case.type, case.is_reversed):
            return True
        else:
            raise ErrorExc

@is_main_group
class MainTestGroup(ValidGroup):
    @property
    def name(self):
        return "Testing:"

    def load(self):
        self.entities = [
            ReadableTests,
            RandomIntTests,
            RandomFloatTests,
            RandomFloatReversedTests,
            RandomPhonebookReversedTests
        ]

class ReadableTests(ValidGroup):
    @property
    def name(self):
        return "Readable Tests"

    def load(self):
        self.entities = [
            Case([1, 10, 100], True, DataFlag.INT),
            Case([3, 2, 1], False, DataFlag.INT),
            Case([5, 6, 3], False, DataFlag.INT),
            Case([("aa", "bb", "cc", 2), ("aa", "bb", "cc", 1)], True, DataFlag.PHONEBOOK),
            Case([("AA", "BB", "CC", 2), ("aa", "bb", "cc", 1)], False, DataFlag.PHONEBOOK),
            Case([("Yana", "Cist", "OleGOVNA", 2281337420), ("Yasha", "Lava", "Petrovna", 420420420)], True, DataFlag.PHONEBOOK),
            Case([("Nill", "Kiggers", "Bullshitovich", 1188811), ("Yuck", "Fu", "Lol", 99999999999)], False, DataFlag.PHONEBOOK)
        ]

class RandomIntTests(ValidGroup):
    @property
    def name(self):
        return "Low Numbers"

    def load(self):
        flag = DataFlag.INT
        is_reversed = False
        self.entities = [generate_case(flag, is_reversed) for _ in range(100)]


def generate_case(flag: DataFlag, is_reversed: bool):
    return Case(generate_data(flag, 50), is_reversed, flag)

class RandomFloatTests(ValidGroup):
    @property
    def name(self):
        return "Random Float Tests"

    def load(self):
        flag = DataFlag.FLOAT
        is_reversed = False
        self.entities = [generate_case(flag, is_reversed) for _ in range(100)]


class RandomFloatReversedTests(ValidGroup):
    @property
    def name(self):
        return "Random Reversed Float Tests"

    def load(self):
        flag = DataFlag.FLOAT
        is_reversed = True
        self.entities = [generate_case(flag, is_reversed) for _ in range(100)]

class RandomPhonebookReversedTests(ValidGroup):
    @property
    def name(self):
        return "Random Reversed Phonebook Tests"

    def load(self):
        flag = DataFlag.PHONEBOOK
        is_reversed = True
        self.entities = [generate_case(flag, is_reversed) for _ in range(100)]
