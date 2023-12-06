import cv2
import numpy as np
import imutils


def getContours(img, original_img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt,10,True)
        if area > 10000:
            cv2.drawContours(original_img, cnt, -1, (0, 255, 0), 3)

contours = []
puzzle = "Sudoku_board.png"
img = cv2.imread(puzzle)

# Turn image into canny

imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7,7),3)
imgCanny = cv2.Canny(imgBlur,35,35)
img_copy = img.copy()
keypoints = cv2.findContours(imgCanny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
#newimg = cv2.drawContours(img_copy, contours, -1,(0,255,0),3)


getContours(imgCanny, img_copy)


cv2.imshow('image', img_copy)
if cv2.waitKey(0) & 0xff == ord('q'):
    cv2.destroyAllWindows()

