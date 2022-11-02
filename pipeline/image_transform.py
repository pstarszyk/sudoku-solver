import numpy as np
import imutils
import cv2
import pytesseract

from config.core import config
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
from typing import List, Tuple

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def locate_board(*, image: np.ndarray) -> np.ndarray:
    '''
    :param image: raw image from camera
    :return: cropped and rotated image of sudoku board only
    find bounding edges of sudoku board and apply linear
    transformation to bounded board to obtain rectangular form
    '''

    # adaptive thresholding
    gray = cv2.cvtColor(
        src=image,
        code=cv2.COLOR_BGR2GRAY
    )
    blurred = cv2.GaussianBlur(
        src=gray,
        ksize=(7, 7),
        sigmaX=3
    )
    thresh = cv2.adaptiveThreshold(
        src=blurred,
        maxValue=255,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY,
        blockSize=11,
        C=2
    )
    thresh = cv2.bitwise_not(
        src=thresh
    )

    # find contours and sort
    contours = cv2.findContours(
        image=thresh,
        mode=cv2.RETR_EXTERNAL,
        method=cv2.CHAIN_APPROX_SIMPLE
    )
    contours = imutils.grab_contours(cnts=contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # loop over the contours
    puzzleCnt = None
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(approx) == 4:
            puzzleCnt = approx
            break
    if puzzleCnt is None:
        raise Exception(("Could not find board."))
    board = four_point_transform(gray, puzzleCnt.reshape(4, 2))
    return board


def extract_digit(*, cell: np.ndarray) -> np.ndarray:
    '''
    :param cell: raw image of cell
    :return: clean cell image with borders removed
    '''
    # apply thresholding
    thresh = cv2.threshold(src=cell,
                           thresh=0,
                           maxval=255,
                           type=cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # clear gridlines near the borders
    thresh = clear_border(labels=thresh)

    # get contours
    cnts = cv2.findContours(image=thresh,
                            mode=cv2.RETR_EXTERNAL,
                            method=cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts=cnts)

    if len(cnts) == 0:
        return None

    # get the largest contour and create mask
    c = max(cnts, key=cv2.contourArea)
    mask = np.zeros(thresh.shape, dtype="uint8")
    cv2.drawContours(mask, [c], -1, 255, -1)

    # check percentage of non-empty pixels
    (h, w) = thresh.shape
    portionFilled = cv2.countNonZero(mask) / float(h * w)
    if portionFilled < config.pipeline_config.percent_fill_thresh:
        return None
    # apply the mask to the thresholded cell
    digit = cv2.bitwise_and(src1=thresh,
                            src2=thresh,
                            mask=mask)
    return digit


def crop_digit(*, digit: np.ndarray) -> np.ndarray:
    '''
    centers the digit and provides fixed buffers on
    side and top to be consistent with all other cells
    :param digit: clean cell image with borders removed
    :return: centered image
    '''

    m, n = digit.shape
    left, right = 0, n - 1
    top, bottom = 0, m - 1

    while left < n:
        if np.sum(digit[:, left]) > 255:
            break
        left += 1
    while right > 0:
        if np.sum(digit[:, right]) > 255:
            break
        right -= 1
    while top < m:
        if np.sum(digit[top, :]) > 255:
            break
        top += 1
    while bottom > 0:
        if np.sum(digit[bottom, :]) > 255:
            break
        bottom -= 1

    y = config.pipeline_config.image_mappings['crop_length_tb']
    x = config.pipeline_config.image_mappings['crop_length_rl']

    cropped_digit = np.zeros((bottom - top + 2 * y, right - left + 2 * x), dtype="uint8")
    cropped_digit[y: (y + bottom - top), x: x + (right - left)] = digit[top: bottom, left: right]
    return cropped_digit


def create_stack(*, digit: np.ndarray) -> np.ndarray:
    stack_size = config.pipeline_config.image_mappings['stack_size']
    digits = np.hstack(tuple(digit for _ in range(stack_size)))
    return digits


def get_num(*, chars: str) -> int:
    freqs = [0] * 9
    nums = int(''.join([x for x in chars if x.isdigit()]))
    while nums:
        num = nums % 10
        freqs[num - 1] += 1
        nums //= 10
    return freqs.index(max(freqs)) + 1


def predict_number(*, digit: np.ndarray) -> int:
    digit_stack = create_stack(digit=digit)
    chars = pytesseract.image_to_string(digit_stack)
    if any(char.isdigit() for char in chars):
        integer = get_num(chars=chars)
        return integer


def extract_array(*, image: np.ndarray) -> Tuple[List[List[int]], np.ndarray]:
    y = config.pipeline_config.image_mappings['resize_y']
    x = config.pipeline_config.image_mappings['resize_x']

    result = [[0 for _ in range(9)] for _ in range(9)]
    image = cv2.resize(src=image,
                       dsize=(x, y),
                       interpolation=cv2.INTER_AREA)
    board = locate_board(image=image)

    vpixels, hpixels = board.shape
    vstep, hstep = vpixels // 9, hpixels // 9
    for row in range(9):
        for col in range(9):
            cell = board[row * vstep:(row + 1) * vstep, col * hstep:(col + 1) * hstep]
            digit = extract_digit(cell=cell)
            if digit is not None:
                digit = crop_digit(digit=digit)
                digit = predict_number(digit=digit)
                if digit is not None:
                    result[row][col] = digit
    return result, board
