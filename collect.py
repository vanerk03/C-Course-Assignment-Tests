from __future__ import annotations
from generate import generate_data, DataFlag, answer
import os
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path

import color_log

main_name = "Тест 3его дз"
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
        # this should be probably removed
        if self.type == "phonebook":
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
        3. Catch exceptions and wrongs. After 'stop_after' failed test will be stopped.
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
                    print(color_log.RED(f"Wrong. Test save in {inp} / {out}"))
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
        raise "MainGroup not run cases."

    def load(self):
        raise "MainGroup have not load."


main_group = MainGroup()


def is_main_group(group_class):
    if not issubclass(group_class, Group):
        raise "is_test_group is decorator for classes, that inherit Group."
    main_group.entities.append(group_class)


"""
Personal classes
"""

class ValidGroup(Group, ABC):
    def _run_case(self, case: Case, inp: Path, out: Path):
        
        with open(inp, "w") as inp_f:
            inp_f.write(str(case))

        subprocess.call([program_name, str(inp), str(out)])

        # here output data should be read then invoke generate.answer method and compare
        with out.open("r") as out_f:
            ans = []
            ot = [x.rstrip("\n") for x in out_f.readlines()]
            
            if case.type == DataFlag.INT:
                ans = answer(map(int, ot), case.is_reversed)

            elif case.type == DataFlag.FLOAT:
                ans = answer(map(float, ot), case.is_reversed)

            elif case.type == DataFlag.PHONEBOOK:
                raise Exception("this is not supported yet")
            print(ans)
            print(case.out)
            if ans == case.out:
                return True
            else:
                raise ErrorExc


class ReadableTests(ValidGroup):
    @property
    def name(self):
        return "Low Numbers"

    def load(self):
        self.entities = [
            Case([1, 10, 100], True, DataFlag.INT),
            Case([3, 2, 1], False, DataFlag.INT),
            Case([5, 6, 3], False, DataFlag.INT)
        ]


class RandomIntTests(ValidGroup):
    @property
    def name(self):
        return "Low Numbers"

    def load(self):
        flag = DataFlag.INT
        is_reversed = False
        self.entities = [generate_case(flag, is_reversed) for _ in range(100)]

@is_main_group
class TestInt(ValidGroup):
    @property
    def name(self):
        return "Numbers"

    def load(self):
        self.entities = [
            Case([1, 10, 100], True, DataFlag.INT),
            Case([3, 2, 1], False, DataFlag.INT),
            Case([5, 6, 3], False, DataFlag.INT)
        ]

def generate_case(flag: DataFlag, is_reversed: bool):
    return Case(generate_data(flag), is_reversed, flag)