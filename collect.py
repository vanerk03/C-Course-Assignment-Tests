from __future__ import annotations

import os
from abc import ABC, abstractmethod
from pathlib import Path

main_name = "Тест 3его дз"
stop_after = 1

"""
Special classes
"""
working_directory = Path(os.getcwd())
program_name: Path


class Case:
    def __init__(self, inp: str, out: str):
        self.inp = inp
        self.out = out


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

        1. Create input.txt output.txt.
        2. Call _run().
        3. Catch exceptions and wrongs. After 10 failed test will be stopped.
        """
        print(" " * self.level + self.name)
        for ent in self.entities:
            if issubclass(type(ent), Case):
                inp = working_directory.joinpath("inp.txt")
                out = working_directory.joinpath("out.txt")
                with inp.open("w"), out.open("w"):
                    pass
                try:
                    self._run_case(ent, inp, out)
                except:
                    print(" " * self.level + f"Wrong actual: {ent.out} expected: {ent.out}")

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
        # todo
        print(f'run {case.inp} {case.out}')
        return True


class TestIntLow(ValidGroup):
    @property
    def name(self):
        return "Low Numbers"

    def load(self):
        self.entities = [
            Case('123', '123'),
            Case('123', '123'),
            Case('123', '123'),
            Case('123', '123'),
        ]


@is_main_group
class TestInt(ValidGroup):
    @property
    def name(self):
        return "Numbers"

    def load(self):
        self.entities = [
            Case('123', '123'),
            Case('123', '123'),
            Case('123', '123'),
            Case('123', '123'),
            TestIntLow
        ]
