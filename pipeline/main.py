from integer_program import solve_board
from tornado.options import define, options
from PIL import Image
import numpy as np
import os
from typing import List
from pprint import pprint
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_PATH = ROOT / 'examples'


def set_environment_variables() -> None:
    path = options.tessdata
    os.environ["TESSDATA_PREFIX"] = path
    if 'C:' in path:
        tesseract = path.replace(r"\tessdata", "")
        os.environ["PATH"] += ";%s" % tesseract


def main() -> List[List[int]]:
    path = EXAMPLE_PATH / options.image_sample
    image = Image.open(path)
    image = np.array(image)
    board, _ = extract_array(image=image)
    solution = solve_board(board=board)
    return solution


if __name__ == "__main__":
    define("tessdata", default=None, type=str, help="Path to tessdata on your machine. ex Windows = C:\Program Files\Tesseract-OCR\tessdata Linux = /usr/share/tesseract-ocr/5/tessdata")
    define("image_sample", default=None, type=str, help="Name of image file in examples folder.")
    options.parse_command_line()
    set_environment_variables()
    from image_transform import extract_array
    result = main()
    pprint(result)
