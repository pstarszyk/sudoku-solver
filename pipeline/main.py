from transforms import extract_array
from solver import solve_board
from tornado.options import define, options
from PIL import Image
import numpy as np
from typing import List
from pprint import pprint
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_PATH = ROOT / 'examples'

# reject images with resolution < x, modify parameters in transforms based on resolution
def main() -> List[List[int]]:
    path = EXAMPLE_PATH / options.image_sample
    image = Image.open(path)
    image = np.array(image)
    board = extract_array(image=image)
    solution = solve_board(board=board)
    return solution


if __name__ == "__main__":
    define("image_sample", default=None, type=str)
    options.parse_command_line()
    res = main()
    pprint(res)
