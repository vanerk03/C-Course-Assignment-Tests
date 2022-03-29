import os
import re
import sys
from pathlib import Path
from subprocess import call, run
from compile import compile_program
from color_log import RED, GREEN

# ----INIT----
# parsing args, write on module argparse
try:
    compiler = sys.argv[1]
    program_name = sys.argv[2]
except IndexError:
    exit("you should write options: compiler_name program_name")

working_directory = Path(os.getcwd())
testing_directory = Path(__file__).parent

program_path = testing_directory.joinpath("program.exe")
cases_directory = testing_directory.joinpath('cases')

compile_program(compiler, working_directory.joinpath(program_name), program_path)


# in future move to special file
# EPS = 0.001
#
# def read_to_array(n, file):
#     array = []
#     a = file.readline().strip(" \n")
#
#     if re.search("solution", a) is not None:
#         return a
#     else:
#         array.append(float(a))
#
#     for _ in range(1, n):
#         elem = float(file.readline())
#         array.append(elem)
#     return array


class Test:
    def __init__(self, num):
        # this is a constructor for an existing Test
        # if you want to generate new one, use testGenerator
        self.num = num

    def run(self, group_name):
        pass
        # result_filename = testing_directory.joinpath("test_output")
        # result = True
        # try:
        #     input_filename = f"{cases_directory}/{group_name}/cases{self.num}.in"
        #     output_filename = f"{cases_directory}/{group_name}/test{self.num}.out"
        #     code_filename = f"{cases_directory}/{group_name}/test{self.num}.code"
        #     result_code = call([program_path, input_filename, result_filename])  # todo timeout
        #
        #     if result_code != 0:
        #         try:
        #             with open(code_filename) as code_file:
        #                 code = int(code_file.read())
        #                 return result_code == code
        #         except IOError:
        #             return False
        #
        #     with open(input_filename, "r") as input_file, \
        #             open(output_filename, "r") as output_file, \
        #             open(result_filename, "r") as current_res:
        #
        #         n = int(input_file.readline())
        #         s = [0] * (n + 1)
        #
        #         for i in range(n):
        #             s[i] = list(map(float, input_file.readline().split()))
        #
        #         x = read_to_array(n, output_file)
        #         correct = read_to_array(n, current_res)
        #         result = self.check(x, correct, n)
        # except ValueError:
        #     result = False
        # except Exception as e:
        #     print("Error: ", e)
        #     result = False
        # finally:
        #     print(f"\tTest {self.num}:".ljust(10), GREEN("Passed") if result else RED("FAILED"))
        #     try:
        #         os.remove(result_filename)
        #     finally:
        #         return result

    def check(self, first, second, n):
        pass
        # if type(first) != type(second):
        #     return False
        #
        # if type(first) == type(second) == str:
        #     return first == second
        #
        # for i in range(n):
        #     if abs(first[i] - second[i]) > EPS:
        #         return False
        # return True


class Group:
    def __init__(self, name, frm, to):
        self.tests = []
        for i in range(frm, to + 1):
            self.tests.append(Test(i))
        self.name = name

    def log(self):
        print(f"\n{self.name} Tests:\n")


class Tester:
    def __init__(self, groups):
        self.groups = groups

    def run(self):
        success = 0
        count = 0
        for group in self.groups:
            group.log()
            for test in group.tests:
                if test.run(group.name):
                    success += 1
                count += 1
        print("\n   " + "-" * 28 + "\n")
        if success == count:
            print("\tTests: PASSED")
        else:
            print("\tTests: FAILED")
            print(f"\tPassed: {success}/{count}")
        print()


# def check_solution(n, coef, var):
#     res = 0
#     for i in range(n):
#         for j in range(n):
#             res += coef[i][j] * var[j]
#         res -= coef[i][n]
#         print(res)
#         if abs(res) > EPS:
#             return False
#     return True


tester = Tester([])
tester.run()
