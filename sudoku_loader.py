import cv2
import imutils
from easyocr import Reader
import numpy as np
import transform
from skimage.segmentation import clear_border
import math


reader = Reader(['en'])
def findPuzzle(img):
    """
    Finds the border of the puzzle
    :param img: Image of board
    :return: Bounding Rectangle of puzzle
    """

    contours = []
    puzzle = img
    img = cv2.imread(puzzle)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3),3)


    #apply threshhold
    thresh = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    #invert thresh
    thresh = cv2.bitwise_not(thresh)


    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(contours)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    #initialize puzzle contour
    puzzleCnt = None
    #finds the largest square shaped contour
    for c in cnts:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*perimeter, True)

        if len(approx) == 4:
            puzzleCnt = approx
            break
    x,y,w,h = cv2.boundingRect(puzzleCnt)
    thresh = transform.fourPointTransform(thresh, puzzleCnt.reshape(4,2))
    #isolates the puzzle from the rest of the image
    cv2.imshow('thresh',thresh)
    if cv2.waitKey(0) & 0xff == ord('q'):
        cv2.destroyAllWindows()
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
    Xstep = thresh.shape[0] // 9
    Ystep = thresh.shape[1] // 9
    for x in range(0,9):
        startX = x * Xstep
        endX = (x + 1) * Xstep
        for y in range(0,9):
            startY = y * Ystep
            endY = (y + 1) * Ystep
            cell = thresh[startX: endX, startY: endY]
            puzzTable[x, y] = extractNumber(cell)
            
    return puzzTable


def cropCell(cell):
    """
    Crops the outer 1/10th of the cell in order to prevent
    the program from mistaking the borders as part of the number.
    It crops more off the sides, because numbers tend to be taller than
    they are wide, and the right and left sides of the box are the most
    likely to cause problems
    param cell: binary outline of cell
    :return: cropped cell
    """
    Xsize = cell.shape[0]
    Ysize = cell.shape[1]
    Xtrim = Xsize // 10
    Ytrim = Ysize // 20
    return cell[Xtrim: Xsize - Xtrim, Ytrim: Ysize - Ytrim]


def extractNumber(thresh):
    """
    param thresh: binary outline of cell
    :return: integer
    """
    thresh = clear_border(thresh)
    text = reader.readtext(thresh, text_threshold = 0.7, allowlist="123456789")
    #handling any blank cells
    
    if len(text) == 0:
        return 0
    if text[0][1] == '':
        return 0
    num = int(text[0][1])
    if num > 9:
        if(num/10 == 1):
            return num%10
        elif(num%10 == 1):
            return num/10
        else:
            return 0
    return num
