import cv2
import numpy as np

def orderPoints(pts):
    """
    Organizes list of points into top right, top left, bottom right, and bottom left
    param pts: list of coordinate
    :return: ordered list of points : (tl, tr, br, bl)
    """
    rect = np.zeros((4, 2), dtype = "float32")
    #top left will have the lowest sum between x and y value
    #bottom right will have the largest sum
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    
    #top right will have the smallest (including negaive) difference between x and y
    #bottom left will have the greatest difference between x and y
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    
    return rect
def fourPointTransform(image, pts):
    """
    Corrects the perspective of a rectangle to be perfectly rectangular
    param image: image]
    param pts: list of 4 points of the rectangle
    :return: image
    """
    rect = orderPoints(pts)
    (tl, tr, br, bl) = rect
    
    #compute the new image, which will be the maximum distance between either the top two corners, or bottom two corners
    widthA = np.sqrt(((br[0]-bl[0]) ** 2) + ((br[1]-bl[1]) ** 2))
    widthB = np.sqrt(((tr[0]-tl[0]) ** 2) + ((tr[1]-tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    
    #compute height of the new image, which will be the maximum distance between left two corners, or the right two corners
    heightA = np.sqrt(((tr[0]-br[0]) ** 2) + ((tr[1]-br[1]) ** 2))
    heightB = np.sqrt(((tl[0]-bl[0]) ** 2) + ((tl[1]-bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    
    #creates array with the dimensions of the new image
    dms = np.array([
        [0,0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype= "float32")

    #calculates the transformation matrix to feed into cv2.warpPerspective
    M = cv2.getPerspectiveTransform(rect, dms)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    
    #return warped image
    return warped
