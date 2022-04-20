from PIL import Image
from pathlib import Path


def png_to_pnm(input_file: Path, output_file: Path):
    if not str(input_file).endswith('.png') and not str(output_file).endswith('.pnm'):
        raise "input, output should ends .png or .pnm"
    im = Image.open(input_file)
    im.save(output_file)


def pnm_to_png(input_file: Path, output_file: Path):
    if not str(input_file).endswith('.pnm') and not str(output_file).endswith('.png'):
        raise "input, output should ends .png or .pnm"
    im = Image.open(input_file)
    im.save(output_file)
