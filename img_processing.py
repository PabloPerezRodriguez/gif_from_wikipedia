import cairosvg
import os
from pathlib import Path

def process_svg(input_file, output_file):
  print(f'Converting {input_file}')
  cairosvg.svg2png(url=input_file, write_to=output_file, dpi=250)
