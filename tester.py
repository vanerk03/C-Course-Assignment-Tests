from io import TextIOWrapper
import os
import re
import sys

try:
    cmpl_msg = sys.argv[1]
    run_msg = sys.argv[2]
except IndexError:
    print("you should run tester from console")
EPS = 0.001

def read_to_array(n: int, file: TextIOWrapper):
    array = []
    a = file.readline().strip(" \n")

    if re.search("solution", a) is not None:
        return a
    else:
        array.append(float(a))

    for _ in range(1, n):
        elem = float(file.readline())
        array.append(elem)
    return array


class Test:
    def __init__(self, num: int, input_file=None, output_file=None):
        # this is a constructor for an existing Test
        # if you want to generate new one, use testGenerator
        self.num = num
        if input_file is None:
            self.input_file = f"tests/test{num}.in"
            self.output_file =  f"tests/test{num}.out"
        else:
            self.input_file = input_file
            self.output_file = output_file

    def run(self):
        result_filename = "test_output"
        result = True
        os.system(f"{run_msg} {self.input_file} {result_filename}")

        with open(self.input_file, "r") as input_file, \
            open(self.output_file, "r") as output_file, \
            open(result_filename, "r") as current_res:
            
            n = int(input_file.readline())
            s = [0] * (n + 1)

            for i in range(n):
                s[i] = list(map(float, input_file.readline().split()))

            x = read_to_array(n, output_file)
            correct = read_to_array(n, current_res)
            result = self.check(x, correct, n)

        print(f"\tTest {self.num}:".ljust(10), "Passed" if result else "FAILED")
        os.remove(result_filename)

        return result


    def check(self, first: object, second: object, n: int):
        if type(first) != type(second):
            return False
        
        if type(first) == type(second) == str:
            return first == second

        for i in range(n):
            if abs(first[i] - second[i]) > EPS:
                return False
        return True

class Group:
    def __init__(self, name: str, frm: int, to: int):
        self.tests = []
        for i in range(frm, to + 1):
            self.tests.append(Test(i))
        self.name = name
    
    def log(self):
        print(f"\n{self.name} Tests:\n")

class Tester:
    def __init__(self, groups: list[Group]):
        self.groups = groups
    
    def run(self):
        success = 0
        count = 0
        for group in self.groups:
            group.log()
            for test in group.tests:
                if test.run():
                    success += 1
                count += 1
        print()
        if success == count:
            print("\tTests: PASSED")
        else:
            print("\tTests: FAILED")
            print(f"\tPassed: {success}/{count}")
        print()


def check_solution(n: int, coef: list[float], var: list[float]):
    res = 0
    for i in range(n):
        for j in range(n):
            res += coef[i][j] * var[j]
        res -= coef[i][n]
        print(res)
        if abs(res) > EPS:
            return False
    return True

os.system(cmpl_msg)

group1 = Group("Google Drive", 1, 13)
group2 = Group("Very Small Number",  14, 53)
group3 = Group("Small Number", 54, 68)
group4 = Group("Moderate Number", 69, 80)
group5 = Group("Moderate Number", 81, 100)
group6 = Group("No solution", 101, 110)
group7 = Group("Many solutions", 111, 140)

groups = [group1, group2, group3, group4, group5, group6, group7]

tester = Tester(groups)
tester.run()