from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

class Sudoku():
    """
    initialize statics
    1. chromeDriver -> location of the chromedriver
    2. website -> sudoku online website
    """
    def __init__(self) -> None:
        self.chromeDriver = webdriver.Chrome(executable_path='./chromedriver')
        self.website = 'https://nine.websudoku.com/?level='
        self.board = []
        self.difficulty = input('#'*20 + '\n' + 'difficulty level (1 to 4) ?: ' + '\n' + '#'*20 + '\n')
        self.website += self.difficulty
        self.chromeDriver.get(self.website)
        time.sleep(2)
        self.getBoard()
        self.rowData, self.colData = self.getData()
    
    def getBoard(self):
        board = []

        for rowIdx in range(9):
            eachRow = []
            for colIdx in range(9):
                try:
                    digit = self.chromeDriver.find_element_by_id(f'f{colIdx}{rowIdx}').get_attribute('value')
                    if digit == '':
                        digit = 0
                except:
                    digit = 0
                finally:
                    digit = int(digit)
                eachRow.append(digit)
            board.append(eachRow)
        
        self.board = board
        return 

    def printBoard(self):
        flag = '#'*8 + 'BOARD::START' + '#'*8
        print(flag)

        for row in self.board:
            print(row)

        flag = '#'*8 + 'BOARD::START' + '#'*8
        print(flag)
        return
    
    def getData(self):
        rowData = {}
        colData = {}
        for rowIdx in range(9):
            for colIdx in range(9):
                digit = self.board[rowIdx][colIdx]

                if rowIdx not in rowData:
                    rowData[rowIdx] = {}
                if colIdx not in colData:
                    colData[colIdx] = {}
                if digit > 0:
                    rowData[rowIdx][digit] = colIdx
                    colData[colIdx][digit] = rowIdx

        print('#'*8 + 'ROWDATA' + '#'*8)
        print(rowData)
        print('#'*8 + 'COLDATA' + '#'*8)
        print(colData)
        
        return rowData, colData
    
    def possible(self, rowIdx, colIdx, digit):
        if self.board[rowIdx][colIdx] > 0:
            return False
        possible = True
        if digit in self.rowData[rowIdx] or digit in self.colData[colIdx]:
            possible = False
        
        subRowStart = 3 * ( rowIdx//3 )
        subColStart = 3 * ( colIdx//3 )
        for row in range(subRowStart, subRowStart + 3):
            for col in range(subColStart, subColStart + 3):
                if self.board[row][col] == digit:
                    possible = False
        return possible
    
    def getOppCoordinate(self, digit, idx, subMatrix, type_):
        subMatrix *= 3
        probInvCoords = []
        for invIdx in range(subMatrix, subMatrix + 3):
            if type_ == 'row' and self.possible(idx, invIdx, digit):
                probInvCoords.append(invIdx)
            if type_ == 'col' and self.possible(invIdx, idx, digit):
                probInvCoords.append(invIdx)
        if len(probInvCoords) == 1:
            return probInvCoords[0]
        return -1
    
    def ruleOfThree(self, board, changes, type_):
        for idx in range(0, 9, 3):
            for digit in range(1, 10):
                oppCoordinates = set([0, 1, 2])
                currCoordinates = []
                for currCoord in range(idx, idx + 3):
                    if type_ == 'row':
                        if digit in self.rowData[currCoord]:
                            oppCoordinate = (self.rowData[currCoord][digit])//3
                            oppCoordinates.remove(oppCoordinate)
                        else:
                            currCoordinates.append(currCoord)

                    
                    if type_ == 'col': 
                        if digit in self.colData[currCoord]:
                            oppCoordinate = (self.colData[currCoord][digit])//3
                            oppCoordinates.remove(oppCoordinate)
                        else:
                            currCoordinates.append(currCoord)
                
                if len(currCoordinates) == 1:
                    x = currCoordinates[0]
                    ySubMatrix = oppCoordinates.pop()
                    y = self.getOppCoordinate(digit, x, ySubMatrix, type_)
                    if y != -1:
                        if type_ == 'row':
                            board[x][y] = digit
                            self.chromeDriver.find_element_by_id(f'f{y}{x}').send_keys(f'{digit}')
                            self.rowData[x][digit] = y
                            self.colData[y][digit] = x
                            self.board = board
                            changes += 1
                        if type_ == 'col':
                            board[y][x] = digit
                            self.chromeDriver.find_element_by_id(f'f{x}{y}').send_keys(f'{digit}')
                            self.rowData[y][digit] = x
                            self.colData[x][digit] = y
                            self.board = board
                            changes += 1

        return changes

    def getProbables(self, board, rowIdx, colIdx):
        probables = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for digit in range(1, 10):
            if not self.possible(rowIdx, colIdx, digit):
                probables.remove(digit)
        return probables

    def fillExactPos(self, board, changes):
        for rowIdx in range(9):
            for colIdx in range(9):
                if board[rowIdx][colIdx] == 0:
                    probableDigits = self.getProbables(board, rowIdx, colIdx)
                    if len(probableDigits) == 1:
                        digit = probableDigits.pop()
                        board[rowIdx][colIdx] = digit
                        self.chromeDriver.find_element_by_id(f'f{colIdx}{rowIdx}').send_keys(f'{digit}')
                        self.rowData[rowIdx][digit] = colIdx
                        self.colData[colIdx][digit] = rowIdx
                        self.board = board
                        changes += 1
        return changes

    def preFillBoard(self, board):
        changes = 0
        changes += self.fillExactPos(board, changes)
        changes += self.ruleOfThree(board, changes, 'row')
        changes += self.ruleOfThree(board, changes, 'col')
        return changes

    def backtrackFillBoard(self, board, rowStart=0, colStart=0):
        # self.chromeDriver.find_element_by_id(f'f{colIdx}{rowIdx}').send_keys(f'{digit}')
        # self.chromeDriver.find_element_by_id(f'f{colIdx}{rowIdx}').send_keys(Keys.BACKSPACE)
        # recursion terminating statement
        if rowStart == 8 and colStart == 8:
            self.board = board
            return True
        for rowIdx in range(rowStart, 9):
            if rowIdx == rowStart:
                iterStart =  colStart
            else:
                iterStart = 0
            for colIdx in range(iterStart, 9):
                if board[rowIdx][colIdx] == 0:
                    for digit in range(1, 10):
                        if self.possible(rowIdx, colIdx, digit):
                            board[rowIdx][colIdx] = digit
                            self.chromeDriver.find_element_by_id(f'f{colIdx}{rowIdx}').send_keys(f'{digit}')
                            self.rowData[rowIdx][digit] = colIdx
                            self.colData[colIdx][digit] = rowIdx

                            

                            #recursive call
                            if colIdx + 1 > 8:
                                isFilled = self.backtrackFillBoard(board, rowIdx + 1, 0)
                            else:
                                isFilled = self.backtrackFillBoard(board, rowIdx, colIdx + 1)
                            if isFilled:
                                return True
                            
                            #if not terminated, then it's false case ==> backtrack
                            board[rowIdx][colIdx] = 0
                            del self.rowData[rowIdx][digit]
                            del self.colData[colIdx][digit]
                            self.chromeDriver.find_element_by_id(f'f{colIdx}{rowIdx}').send_keys(Keys.BACKSPACE)
                        
                    return False
    
    def completeFillBoard(self):
        changes = 1
        while changes > 0:
            changes = self.preFillBoard(self.board)
        self.backtrackFillBoard(self.board)
        time.sleep(20)
        self.chromeDriver.close()
        self.printBoard()
        return
if __name__ == "__main__":
    # initialize the board
    board = Sudoku()

    #solve the puzzle
    board.completeFillBoard()