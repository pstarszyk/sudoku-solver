import numpy as np
import imutils
import cv2
import pytesseract

from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
from typing import List

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def locate_board(*, image: np.ndarray) -> np.ndarray:
    '''
    find bounding edges of sudoku board and apply linear
    transformation to bounded board to obtain rectangular form
    :param image:
    :return:
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
    # apply automatic thresholding to the cell and then clear any
    # connected borders that touch the border of the cell
    thresh = cv2.threshold(cell, 0, 255,
                           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    thresh = clear_border(thresh)
    # find contours in the thresholded cell
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # if no contours were found than this is an empty cell
    if len(cnts) == 0:
        return None
    # otherwise, find the largest contour in the cell and create a
    # mask for the contour
    c = max(cnts, key=cv2.contourArea)
    mask = np.zeros(thresh.shape, dtype="uint8")
    cv2.drawContours(mask, [c], -1, 255, -1)
    # compute the percentage of masked pixels relative to the total
    # area of the image
    (h, w) = thresh.shape
    percentFilled = cv2.countNonZero(mask) / float(w * h)
    # if less than 3% of the mask is filled then we are looking at
    # noise and can safely ignore the contour
    if percentFilled < 0.03:
        return None
    # apply the mask to the thresholded cell
    digit = cv2.bitwise_and(thresh, thresh, mask=mask)
    # check to see if we should visualize the masking step
    # return the digit to the calling function
    return digit


def crop_digit(*, digit: np.ndarray) -> np.ndarray:
    '''

    :param digit:
    :return:
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

    cropped_digit = np.zeros((bottom - top + 2 * 20, right - left + 2 * 5), dtype="uint8")
    cropped_digit[20: (20 + bottom - top), 5: 5 + (right - left)] = digit[top: bottom, left: right]
    return cropped_digit


def create_stack(*, digit: np.ndarray) -> np.ndarray:
    digits = np.hstack(tuple(digit for _ in range(5)))
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
    #digit = 255 - digit
    digit_stack = create_stack(digit=digit)
    chars = pytesseract.image_to_string(digit_stack)
    #print(chars)
    if any(char.isdigit() for char in chars):
        integer = get_num(chars=chars)
        #print(integer)
        return integer
    return


def extract_array(*, image: np.ndarray) -> List[List[int]]:
    result = [[0 for _ in range(9)] for _ in range(9)]
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
    return result
