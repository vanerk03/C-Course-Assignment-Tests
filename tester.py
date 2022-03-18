from io import TextIOWrapper
import os
import re
import sys

cmpl_msg = ""
run_msg = ""

try:
    cmpl_msg = sys.argv[1]
    run_msg = sys.argv[2]
except IndexError:
    exit("you should run tester from console")
    
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
    def __init__(self, num: int):
        # this is a constructor for an existing Test
        # if you want to generate new one, use testGenerator
        self.num = num

    def run(self, group_name: str):
        result_filename = "test_output"
        result = True
        try:
            input_filename = f"tests/{group_name}/test{self.num}.in"
            output_filename = f"tests/{group_name}/test{self.num}.out"

            os.system(f"{run_msg} \"{input_filename}\" {result_filename}")

            with open(input_filename, "r") as input_file, \
                open(output_filename, "r") as output_file, \
                open(result_filename, "r") as current_res:
                
                n = int(input_file.readline())
                s = [0] * (n + 1)

                for i in range(n):
                    s[i] = list(map(float, input_file.readline().split()))

                x = read_to_array(n, output_file)
                correct = read_to_array(n, current_res)
                result = self.check(x, correct, n)
        except ValueError:
            result = False
        finally:
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
                if test.run(group.name):
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
group8 = Group("Eps", 141, 160)
group9 = Group("Small floats", 161, 200)
group10 = Group("Combining large and small numbers", 201, 210)

groups = [group1, group2, group3, group4, group5, group6, group7, group8, group9, group10]

tester = Tester(groups)
tester.run()