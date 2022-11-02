from typing import List
import numpy as np
import cv2


def generate_content(
        *,
        board: List[List[int]],
        solution: List[List[int]],
        output: np.ndarray
) -> np.ndarray:

    vpixels, hpixels = output.shape
    vstep, hstep = vpixels // 9, hpixels // 9
    vshift, hshift = vstep // 6, hstep // 3
    overlay = output.copy()

    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                bottom_left = (col * hstep + hshift, (row + 1) * vstep - vshift)
                overlay = cv2.putText(img=overlay,
                                      text=str(solution[row][col]),
                                      org=bottom_left,
                                      fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                      fontScale=1.5,
                                      color=(255, 0, 0),
                                      thickness=3,
                                      lineType=cv2.LINE_AA)
    return overlay
