from __future__ import annotations

import os
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path

import color_log
from colorama import Fore
from generate import convert_data_to_string, generate_case, solve

main_name = "All tests"

"""
Special classes
"""
working_directory = Path(os.getcwd())
testing_directory = Path(__file__).parent
program_name: Path


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
                    print(color_log.RED(f"FAILED format exception \nComment: {e.message}"))
                    print(color_log.RED(f"Test is saved in {inp} / {out}"))
                    exit()


            elif issubclass(ent, Group):
                _ent = ent(level = self.level + 1)
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


# Readable tests
class SolvedCase(Case):
    def __init__(self, inp: str, out: str):
        self.inp = inp
        self.out = out


@is_main_group
class ReadableTests(Group):
    @property
    def name(self):
        return "Readable Tests"

    def _run_case(self, case: SolvedCase, inp: Path, out: Path):
        with open(inp, "w") as inp_f, open(out, 'w'):
            inp_f.write(case.inp)

        subprocess.call([program_name, str(inp), str(out)])

        with open(out, 'r') as out_f:
            ans = out_f.read()

        # correct output
        ans = ans.strip().split('\n')
        if len(ans[0]) == 2:
            if ans[0] != '-' or not ans[1].isdigit():
                raise ErrorFormatExc('first symbol uncorrected')
        elif len(ans[0]) != 1:
            raise ErrorFormatExc('first symbol uncorrected')
        elif not ans[0].isdigit():
            raise ErrorFormatExc('first symbol uncorrected')

        for i in ans[1:]:
            if len(i) != 1:
                raise ErrorFormatExc('string has more one symbol')
            if not i.isdigit():
                raise ErrorFormatExc('symbol in string is not digit')

        if case.out == ''.join(ans):
            return True
        else:
            raise ErrorExc

    def load(self):
        self.entities = [
            SolvedCase(convert_data_to_string([232, '+', 6, '-', -1]), '12'),
            SolvedCase(convert_data_to_string([1, '+', 1]), '2'),
            SolvedCase(convert_data_to_string([1, '-', 1]), '0'),
            SolvedCase(convert_data_to_string([1, '+', 1, '-', -1]), '3'),
            SolvedCase(convert_data_to_string([2, '*', 3]), '6'),
            SolvedCase(convert_data_to_string([2, '*', 0]), '0'),
            SolvedCase(convert_data_to_string([0, '*', 0]), '0'),
            SolvedCase(convert_data_to_string([0, '/', 1]), '0'),
            SolvedCase(convert_data_to_string([2, '/', 1]), '2'),
            SolvedCase(convert_data_to_string([2, '/', 2]), '1'),
            # todo: need more tests
        ]


class ValidCase(Case):
    def __init__(self, data: list[int | str]):
        self.data = data
        self.correct_answer = solve(data)

    def __str__(self):
        return "\n".join(map(str, self.data))


class ValidGroup(Group, ABC):
    def _run_case(self, case: ValidCase, inp: Path, out: Path):

        with open(inp, "w") as inp_f:
            inp_f.write(str(case))

        subprocess.call([program_name, str(inp), str(out)])
        with open(out) as user_output_file:
            user_output = list(map(int, user_output_file.readlines()))
        
        return user_output == case.correct_answer 

class RandomTests(ValidGroup):
    @property
    def name(self):
        return "Low Numbers"

    def load(self):
        self.entities = [generate_case(5) for _ in range(100)]


@is_main_group
class MainTestGroup(ValidGroup):
    @property
    def name(self):
        return "Testing"

    def load(self):
        self.entities = [
            RandomTests,
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

        print(Fore.LIGHTBLACK_EX, end = '')
        out = subprocess.call(args)
        print(Fore.RESET, end = '')
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


class CantFindFile(ReadableTests):
    @property
    def name(self):
        return "FileNotFound"

    def _run_case(self, case: ValidCase, inp: Path, out: Path):
        args = [str(program_name), str(working_directory.joinpath("qweqweasd.txt")),
                str(working_directory.joinpath("asdasdasdasd.txt"))]
        print(Fore.LIGHTBLACK_EX, end = '')
        out = subprocess.call(args)
        print(Fore.RESET, end = '')
        if out != 1:
            print(color_log.RED(
                f"Excepted return code 1, on command {' '.join(args)}"))
            raise ErrorExc


class ConsoleOutput(ReadableTests):
    name = "Console output"

    def _run_case(self, case: ValidCase, inp: Path, out: Path):
        with open(inp, "w") as inp_f:
            inp_f.write(str(case))

        subprocess.call([str(program_name), str(inp), str(out)],
                        stdout = working_directory.joinpath("stdout.txt").open("w"))

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
        args = ['clang-format', '-style=file', '--dry-run', '-Werror', '.\main.cpp', '.\phonebook.cpp', '.\quicksort.h',
                '.\phonebook.h']
        subprocess.call(args)

    def load(self):
        if not no_error:
            self.entities = [
                Case()
            ]
