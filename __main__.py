import os
import sys
from pathlib import Path
import collect

import updater

# ----INIT----
# parsing args, write in module argparse
program_name = "main"
try:
    program_name = sys.argv[1]
    if '-ner' in sys.argv:
        collect.no_error = True
    if '-fm' in sys.argv:
        collect.format_check = True


except IndexError:
    exit("Not enough arguments")

working_directory = Path(os.getcwd())
testing_directory = Path(__file__).parent

collect.program_name = working_directory.joinpath(program_name)
collect.main_group.run()
