import cv2
import imutils
from easyocr import Reader
import numpy as np


reader = Reader(['en'])
def findPuzzle(img):
    """
    Finds the border of the puzzle
    :param img: Image of board
    :return: Bounding Rectangle of puzzle
    """

    contours = []
    puzzle = "Sudoku_board.png"
    img = cv2.imread(puzzle)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7,7),3)


    #apply threshhold
    thresh = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    #invert thresh
    thresh = cv2.bitwise_not(thresh)


    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(contours)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    #initialize puzzle contour
    puzzleCnt = None

    for c in cnts:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*perimeter, True)

        if len(approx) == 4:
            puzzleCnt = approx
            break
    x,y,w,h = cv2.boundingRect(puzzleCnt)

    thresh = thresh[x: x + w, y: y + h]

    return thresh


def findCells(thresh):
    """
    Splits puzzle into individual cells
    Uses extractNumber() to identify the number in the cell, then puts that info in a table
    :param thresh: cropped-image
    :return: 9x9 list of integers
    """
    puzzTable = np.zeros((9, 9), dtype="int")

    #iterate through each cell and fill in array at the same time
    #create is blank function that uses thresh
    thresh_copy = thresh.copy()
    Xstep = thresh.shape[1] // 9
    Ystep = thresh.shape[0] // 9
    for x in range(0,9):
        startX = x * Xstep
        endX = startX + Xstep
        for y in range(0,9):
            startY = y * Ystep
            endY = startY + Ystep
            cell = thresh[startX: endX, startY: endY]
            puzzTable[x, y] = extractNumber(cell)
    return puzzTable





if cv2.waitKey(0) & 0xff == ord('q'):
    cv2.destroyAllWindows()

def extractNumber(cell):
    """
    param thresh: binary outline of cell
    :return: integer
    """
    text = reader.readtext(cell, mag_ratio=2.0, allowlist="0123456789")

    if len(text) == 0:
        return 0
    print(text[0][1])
    return int(text[0][1])