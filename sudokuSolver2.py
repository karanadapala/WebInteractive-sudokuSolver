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
        self.getBoard(self.chromeDriver, self.website)
    
    def getBoard(self, chromeDriver, website):
        difficulty = input('difficulty level (1 to 4) ?: ')
        chromeDriver.get(website + difficulty)
        time.sleep(2)
        board = []

        for rowIdx in range(9):
            eachRow = []
            for colIdx in range(9):
                try:
                    digit = chromeDriver.find_element_by_id(f'f{colIdx}{rowIdx}').get_attribute('value')
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
    
if __name__ == "__main__":
    # initialize the board
    board = Sudoku()

    # get the live board from the website
    board.getBoard(board.chromeDriver, board.website)
    board.printBoard()