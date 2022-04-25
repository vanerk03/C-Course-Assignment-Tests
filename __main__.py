import os
import sys
from pathlib import Path
import collect
from subprocess import call

call(["git", "pull"], cwd='SkakovLabO4ka')

# ----INIT----
# parsing args, write on module argparse
program_name = "main"
try:
    program_name = sys.argv[1]

    if '-nf' in sys.argv:
        collect.no_float = True
    if '-nfp' in sys.argv:
        collect.no_phonebook = True
    if '-ner' in sys.argv:
        collect.no_error = True
    if '-fm' in sys.argv:
        collect.format_check = True


except IndexError:
    exit("you should write options: program_name")

working_directory = Path(os.getcwd())
testing_directory = Path(__file__).parent

collect.program_name = working_directory.joinpath(program_name)
collect.main_group.run()
