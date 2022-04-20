import os
import sys
from pathlib import Path
from compile import compile_program

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
cases_directory = testing_directory.joinpath('tests')

compile_program(compiler, working_directory.joinpath(program_name), program_path)


# in future move to special file
EPS = 0.001

