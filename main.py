import sudoku_loader as sl
import sudoku_Solver as ss
import easyocr
import cv2
import imutils  
import os

# for filename in os.listdir('Test Puzzles'):
#     puzzle = os.path.join('Test Puzzles', filename)
    
puzzle = 'Test Puzzles\Sudoku_board.png'


board = sl.findPuzzle(puzzle)
table = sl.findCells(board)

print(table)
print("\n")
ss.solve(table)
print(table)
