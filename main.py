import sudoku_loader as sl
import sudoku_Solver as ss
import easyocr
import cv2
import imutils

puzzle = "Sudoku_board.png"



board = sl.findPuzzle(puzzle)
table = sl.findCells(board)

print(table)
print("\n")
ss.solve(table)
print(table)
