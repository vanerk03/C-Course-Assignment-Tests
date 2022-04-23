from __future__ import annotations
from generate import *
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

        return  f"{self.type}\n" \
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


# class SortCase(Case):
#     def __init__(self, type: DataFlag, is_reversed: bool, data: list):
#         data_inp = "\n".join(map(str, data))
#         # inp = f"{type}\n" \
#         #       f"{'ascending' if mode else 'descending'}\n" \
#         #       f"{len(data)}\n" \
#         #       f"{data_inp}"
#         super().__init__(data, is_reversed)


class ValidGroup(Group, ABC):
    def _run_case(self, case: Case, inp: Path, out: Path):
        with inp.open("w") as inp_f, out.open("w") as out_f:
            inp_f.write(str(case))

        subprocess.call(['python', str(program_name), str(inp), str(out)])
        answer_data = out.open("r").readlines()
        # here output data should be read then invoke generate.answer method and compare
        with out.open("r") as out_f:
            ot = out_f.read()
            if ot == case.out:
                return True
            else:
                raise ErrorExc


class ReadableTests(ValidGroup):
    @property
    def name(self):
        return "Low Numbers"

    def load(self):
        self.entities = [
            Case([1, 10, 100], True, DataFlag.INT)
            # Case('float', True, [3.3, 2.2, 2.2, 2.2, 1.1], [1.1, 2.2, 2.2, 2.2, 3.3]),
            #
            # Case('phonebook', False, [1, 1, 1], [1, 1, 1]),
            # Case('int', True, [1, 1, 1], [1, 1, 1]),
            #
            # Case('int', True, [1, 1, 1, 3], [1, 1, 1, 3]),
            # Case('int', False, [1, 1, 1, 3], [3, 1, 1, 1]),
        ]


# class TestIntLow(ValidGroup):
#     @property
#     def name(self):
#         return "Low Numbers"
#
#     def load(self):
#         self.entities = [
#             SortCase('int', True, [1, 10, 100], [1, 10, 100]),
#             SortCase('int', True, [3, 2, 2, 2, 1], [1, 2, 2, 2, 3]),
#
#             SortCase('int', False, [1, 1, 1], [1, 1, 1]),
#             SortCase('int', True, [1, 1, 1], [1, 1, 1]),
#
#             SortCase('int', True, [1, 1, 1, 3], [1, 1, 1, 3]),
#             SortCase('int', False, [1, 1, 1, 3], [3, 1, 1, 1]),
#         ]


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
            SortCase('int', True, [1, 2, 3], [1, 2, 3]),
            SortCase('int', True, [3, 2, 1], [1, 2, 3]),
            SortCase('int', False, [1, 2, 3], [3, 2, 1]),
            SortCase('int', False, [3, 2, 1], [3, 2, 1]),
            TestIntLow
        ]

        # for i in range(100):
        #     self.entities.append(SortCase('int', False, , ))
