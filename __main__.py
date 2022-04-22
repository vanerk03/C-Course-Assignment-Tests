import os
import sys
from pathlib import Path
import collect

# ----INIT----
# parsing args, write on module argparse
program_name = "main"
try:
    program_name = sys.argv[1]
except IndexError:
    exit("you should write options: program_name")

working_directory = Path(os.getcwd())
testing_directory = Path(__file__).parent

collect.program_name = working_directory.joinpath(program_name)
collect.main_group.run()
