from subprocess import run
from pathlib import Path
from color_log import RED


def compile_program(compiler: str, input_path: Path, output_path: Path):
    command = [compiler, str(input_path), '-o', str(output_path)]
    run(command)
    if not output_path.is_file():
        RED(f'Error, cant compile program. \nCommand:{" ".join(command)}')
        exit()
