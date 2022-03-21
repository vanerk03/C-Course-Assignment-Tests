from subprocess import run
from pathlib import Path


def compile_program(compiler: str, input_path: Path, output_path: Path):
    command = [compiler, str(input_path), '-o', str(output_path)]
    run(command)
    if not output_path.is_file():
        exit(f'Error, cant compile program. \nCommand:{" ".join(command)}')
