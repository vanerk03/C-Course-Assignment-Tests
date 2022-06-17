from __future__ import annotations

import os
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path

import color_log
from colorama import Fore
from generate import generate_data, solve, NAN

main_name = "All tests"

"""
Special classes
"""
working_directory = Path(os.getcwd())
testing_directory = Path(__file__).parent
program_name: Path


def generate_case(sz: int = 50, digit_cnt: int = 1):
    tmp = generate_data(sz, digit_cnt, digit_cnt)
    return ValidCase(tmp)


class StopExc(Exception):
    pass


class TrueExc(Exception):
    pass


class ErrorExc(Exception):
    pass


class ErrorFormatExc(Exception):
    def __init__(self, message):
        self.message = message


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

                except ErrorFormatExc as e:
                    print(color_log.RED(
                        f"FAILED format exception \nComment: {e.message}"))
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
no_error = False


class ValidCase(Case):
    def __init__(self, data: list, ans: list = None):
        self.data = data
        if ans is None:
            self.correct_answer = solve(data)
        else:
            self.correct_answer = ans

    def __str__(self):
        return "\n".join(map(str, self.data))


class ValidGroup(Group, ABC):
    def _run_case(self, case: ValidCase, inp: Path, out: Path):
        with open(inp, "w") as inp_f:
            inp_f.write(str(case))

        subprocess.call([program_name, str(inp), str(out)])
        with open(out) as user_output_file:
            user_output = list(map(lambda x: x.rstrip() if x.rstrip() == "NaN"
                                   else int(x), user_output_file.readlines()))
        if user_output != case.correct_answer:
            raise ErrorExc


class ReadableTests(ValidGroup):
    @property
    def name(self):
        return "Readable Tests"

    def load(self):
        self.entities = [
            ValidCase([1, 6, '-'], [-5]),
            ValidCase([2, 2, '+'], [4]),
            ValidCase([4, 2, '/'], [2]),
            ValidCase([6, 6, '+'], [12]),
            ValidCase([6, 0, '/'], ["NaN"]),
            ValidCase([-100, '~'], ["NaN"]),
        ]

class SmallTests(ValidGroup):
    @property
    def name(self):
        return "Small Tests"

    def load(self):
        self.entities = [generate_case(2, 2) for _ in range(200)]

class BigTests(ValidGroup):
    @property
    def name(self):
        return "Big Tests"

    def load(self):
        self.entities = [generate_case(5, 10) for _ in range(10)]


class LargeTests(ValidGroup):
    @property
    def name(self):
        return "Large Tests"

    def load(self):
        self.entities = [generate_case(15, 4) for _ in range(10)]


class TremendousTests(ValidGroup):
    @property
    def name(self):
        return "Tremendous Tests"

    def load(self):
        self.entities = [generate_case(50, 5) for _ in range(10)]


class VerenyaTests(ValidGroup):
    @property
    def name(self):
        return "Verenya Tests"

    def load(self):
        self.entities = [generate_case(50, 30) for _ in range(3)]


@is_main_group
class MainTestGroup(ValidGroup):
    @property
    def name(self):
        return "Testing"

    def load(self):
        self.entities = [
            ReadableTests,
            SmallTests,
            BigTests,
            LargeTests,
            TremendousTests,
            VerenyaTests
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
            # InvalidParamCase(0, [1, 10, 100], True, DataFlag.INT),
            # InvalidParamCase(1, [1, 10, 100], True, DataFlag.INT),
            # InvalidParamCase(3, [1, 10, 100], True, DataFlag.INT),
            # InvalidParamCase(4, [1, 10, 100], True, DataFlag.INT)
        ]

# class CantFindFile(ReadableTests):
#     @property
#     def name(self):
#         return "FileNotFound"

#     def _run_case(self, case: ValidCase, inp: Path, out: Path):
#         args = [str(program_name), str(working_directory.joinpath("qweqweasd.txt")),
#                 str(working_directory.joinpath("asdasdasdasd.txt"))]
#         print(Fore.LIGHTBLACK_EX, end = '')
#         out = subprocess.call(args)
#         print(Fore.RESET, end = '')
#         if out != 1:
#             print(color_log.RED(
#                 f"Excepted return code 1, on command {' '.join(args)}"))
#             raise ErrorExc


# class ConsoleOutput(ReadableTests):
#     name = "Console output"

#     def _run_case(self, case: ValidCase, inp: Path, out: Path):
#         with open(inp, "w") as inp_f:
#             inp_f.write(str(case))

#         subprocess.call([str(program_name), str(inp), str(out)],
#                         stdout = working_directory.joinpath("stdout.txt").open("w"))

#         with working_directory.joinpath("stdout.txt").open("r") as stdout:
#             if len(stdout.read()) != 0:
#                 print(color_log.RED(f"Result should not be written in stdout.txt"))
#                 raise ErrorExc
#         try:
#             os.remove("stdout.txt")
#         except FileNotFoundError:
#             pass


# @is_main_group
# class InvalidGroup(Group, ABC):
#     @property
#     def name(self):
#         return "Errors testing"

#     def _run_case(self, case: Case, inp: Path, out: Path):
#         pass

#     def load(self):
#         if not no_error:
#             self.entities = [
#                 InvalidParams,
#                 CantFindFile,
#                 ConsoleOutput
#             ]


# @is_main_group
# class CheckClangFormat(Group, ABC):
#     @property
#     def name(self):
#         return ".clang-format check | not for all"

#     def _run_case(self, case: Case, inp: Path, out: Path):
#         args = ['clang-format', '-style=file', '--dry-run', '-Werror', '.\main.cpp', '.\phonebook.cpp', '.\quicksort.h',
#                 '.\phonebook.h']
#         subprocess.call(args)

#     def load(self):
#         if not no_error:
#             self.entities = [
#                 Case()
#             ]
