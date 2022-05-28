from __future__ import annotations

import os
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from random import choice
from time import time

import color_log
from colorama import Fore
from generate import generate_data, DataFlag, answer
from solve import solve

main_name = "All tests"


def generate_case(flag: DataFlag, is_reversed: bool, sz:int=50):
    return ValidCase(generate_data(flag, sz), is_reversed, flag)


"""
Special classes
"""
working_directory = Path(os.getcwd())
program_name: Path


class StopExc(Exception):
    pass


class TrueExc(Exception):
    pass


class ErrorExc(Exception):
    pass


class Case:
    pass


class Group(ABC):
    """
    This structure is a superclass that stores both groups and cases. 
    And run cases.
    """

    @property
    @abstractmethod
    def name(self):
        """This method should return information about the group."""

    def __init__(self, level=0):
        self.entities = []
        self.return_code = 0
        self.level = level

    @abstractmethod
    def _run_case(self, case: Case, inp: Path, out: Path):
        """This method should start and check one case, without unexpected exceptions."""

    @abstractmethod
    def load(self):
        """This method should add entities(cases or groups) in self.entities."""

    def run(self):
        """
        This method:

        1. Create input.txt output.txt, don't write.
        2. Call _run().
        3. Catch exceptions and wrong answerss. After 1 failed test, testing will resume.
        """
        global current_error
        print("   " * self.level + self.name + ":")

        for ent in self.entities:
            if issubclass(type(ent), Case):
                inp = working_directory.joinpath(f"inp.txt")
                out = working_directory.joinpath(f"out.txt")
                try:
                    self._run_case(ent, inp, out)
                    try:
                        os.remove(inp)
                        os.remove(out)
                    except FileNotFoundError:
                        pass
                except ErrorExc:
                    print(color_log.RED("FAILED"))
                    print(color_log.RED(f"Test is saved in {inp} / {out}"))
                    exit()

            elif issubclass(ent, Group):
                _ent = ent(level=self.level + 1)
                _ent.load()
                _ent.run()

        print(color_log.GREEN("   " * (self.level + 1) + "Passed\n"))


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
no_float = False
no_phonebook = False
no_error = False
format_check = False


class ValidCase(Case):
    def __init__(self, data: list[int | float | tuple[str, str, str, int]], is_reversed: bool, _type: DataFlag):
        self.data = data
        self.is_reversed = is_reversed
        self.out = answer(data, is_reversed)
        self.type = _type

    def __repr__(self):
        if self.type == DataFlag.PHONEBOOK:
            string = "\n".join(map(lambda x: " ".join(map(str, x)), self.data))
        else:
            string = "\n".join(map(str, self.data))

        return f"{self.type.value}\n" \
               f"{'descending' if self.is_reversed else 'ascending'}\n" \
               f"{len(self.data)}\n" \
               f"{string}"


class ValidGroup(Group, ABC):
    def _run_case(self, case: ValidCase, inp: Path, out: Path):

        with open(inp, "w") as inp_f:
            inp_f.write(str(case))

        subprocess.call([program_name, str(inp), str(out)])

        try:
            _sl = solve(out, case.type, case.is_reversed)
        except Exception:
            raise ErrorExc

        if case.out == _sl:
            return True
        else:
            raise ErrorExc


class ReadableTests(ValidGroup):
    @property
    def name(self):
        return "Readable Tests"

    def load(self):
        self.entities = [
            ValidCase([1, 10, 100], True, DataFlag.INT),
            ValidCase([3, 2, 1], False, DataFlag.INT),
            ValidCase([5, 6, 3], False, DataFlag.INT),
            ValidCase([], False, DataFlag.INT),
            ValidCase([], True, DataFlag.INT)
        ]

        if not no_phonebook:
            self.entities += [
                ValidCase([("aa", "bb", "cc", 2), ("aa", "bb",
                          "cc", 1)], True, DataFlag.PHONEBOOK),
                ValidCase([("AA", "BB", "CC", 2), ("aa", "bb", "cc", 1)],
                          False, DataFlag.PHONEBOOK),
                ValidCase([("Elon", "Musk", "Johnnovich", 2281337420), ("Nazarov", "Vladimir", "Alexeevich", 420420420)], True,
                          DataFlag.PHONEBOOK),
                ValidCase([("Skakov", "Pavlik", "Sergeich", 1188811), ("Kanistr", "Yoda", "Anatolyevich", 99999999999)], False,
                          DataFlag.PHONEBOOK)
            ]


class TimeLimitTests(ValidGroup):
    @property
    def name(self):
        return "TimeLimitTests"

    def _run_case(self, case: ValidCase, inp: Path, out: Path):

        with open(inp, "w") as inp_f:
            inp_f.write(str(case))
        
        start = time()
        subprocess.call([program_name, str(inp), str(out)])
        end = time()
        print(" " * 20 + "Finished in:", round(end - start, 4), "sec")
        try:
            _sl = solve(out, case.type, case.is_reversed)
        except Exception:
            raise ErrorExc

        if case.out == _sl:
            return True
        else:
            raise ErrorExc

    def load(self):
        flag = DataFlag.INT
        is_reversed = True
        self.entities = [generate_case(flag, is_reversed, 5_000_000) for _ in range(5)]

class RandomIntTests(ValidGroup):
    @property
    def name(self):
        return "Low Numbers"

    def load(self):
        flag = DataFlag.INT
        is_reversed = False
        self.entities = [generate_case(flag, is_reversed) for _ in range(100)]


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


class Random(ValidGroup):
    """
    This class generates tests
    """

    def __init__(self, number_of_tests: int, flag: DataFlag, level=0):
        self.number_of_tests = number_of_tests
        self.is_reversed = choice([True, False])
        self.flag = flag
        super().__init__(level)

    @property
    def name(self):
        return "Random tests"

    def load(self):
        self.entities = [generate_case(
            self.flag, self.is_reversed) for _ in range(100)]


@is_main_group
class MainTestGroup(ValidGroup):
    @property
    def name(self):
        return "Testing"

    def load(self):
        self.entities = [
            ReadableTests,
            RandomIntTests,
            TimeLimitTests
        ]
        if not no_float:
            self.entities += [
                RandomFloatTests,
                RandomFloatReversedTests
            ]
        if not no_phonebook:
            self.entities += [
                RandomPhonebookReversedTests,
            ]


# Error handling
class InvalidParamCase(ValidCase):
    def __init__(self, count: int, *args, **kwargs):
        self.count = count
        super().__init__(*args, **kwargs)


class InvalidParams(Group, ABC):
    @property
    def name(self):
        return "Invalid params"

    def _run_case(self, case: InvalidParamCase, inp: Path, out: Path):

        with open(inp, "w") as inp_f:
            inp_f.write(str(case))

        args = [str(program_name)]
        for i in range(case.count):
            args.append("qweasdqweasd")

        print(Fore.LIGHTBLACK_EX, end='')
        out = subprocess.call(args)
        print(Fore.RESET, end='')
        if out != 4:
            print(color_log.RED(
                f"Excepted return code 4, on command {' '.join(args)}"))
            raise ErrorExc

    def load(self):
        self.entities = [
            InvalidParamCase(0, [1, 10, 100], True, DataFlag.INT),
            InvalidParamCase(1, [1, 10, 100], True, DataFlag.INT),
            InvalidParamCase(3, [1, 10, 100], True, DataFlag.INT),
            InvalidParamCase(4, [1, 10, 100], True, DataFlag.INT)
        ]


class CantFindFile(ReadableTests):
    @property
    def name(self):
        return "FileNotFound"

    def _run_case(self, case: ValidCase, inp: Path, out: Path):
        args = [str(program_name), str(working_directory.joinpath("qweqweasd.txt")),
                str(working_directory.joinpath("asdasdasdasd.txt"))]
        print(Fore.LIGHTBLACK_EX, end='')
        out = subprocess.call(args)
        print(Fore.RESET, end='')
        if out != 1:
            print(color_log.RED(
                f"Excepted return code 1, on command {' '.join(args)}"))
            raise ErrorExc


class ConsoleOutput(ReadableTests):
    @property
    def name(self):
        return "Console output"

    def _run_case(self, case: ValidCase, inp: Path, out: Path):
        with open(inp, "w") as inp_f:
            inp_f.write(str(case))

        subprocess.call([str(program_name), str(inp), str(out)],
                        stdout=working_directory.joinpath("stdout.txt").open("w"))

        with working_directory.joinpath("stdout.txt").open("r") as stdout:
            if len(stdout.read()) != 0:
                print(color_log.RED(f"Result should not be written in stdout.txt"))
                raise ErrorExc
        try:
            os.remove("stdout.txt")
        except FileNotFoundError:
            pass


@is_main_group
class InvalidGroup(Group, ABC):
    @property
    def name(self):
        return "Errors testing"

    def _run_case(self, case: Case, inp: Path, out: Path):
        pass

    def load(self):
        if not no_error:
            self.entities = [
                InvalidParams,
                CantFindFile,
                ConsoleOutput
            ]


@is_main_group
class CheckClangFormat(Group, ABC):
    @property
    def name(self):
        return ".clang-format check | not for all"

    def _run_case(self, case: Case, inp: Path, out: Path):
        subprocess.call(
            ['clang-format', '-style=file', '--dry-run', '-Werror', '.\main.cpp', '.\phonebook.cpp', '.\quicksort.h',
             '.\phonebook.h'])

    def load(self):
        if not no_error:
            if format_check:
                self.entities = [
                    Case()
                ]
