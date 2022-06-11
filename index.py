import random


class Game:
    def __init__(self, board) -> None:
        self.drawer = Drawer()
        self.board = board
        self.play()
    
    def play(self):
        self.drawer.draw(self.board)

        action = input('Select action (Flag, Click): ')
        if action not in ['Flag', 'Click']:
            print(action + ' is not a valid action, please select either Flag or Click')
            self.play()

        row = int(input('Select row: ')) - 1
        column = int(input('Select column: ')) - 1

        try:
            if action == 'Flag':
                self.board.flagCell(row, column);
                self.play()
                return
            else:
                self.board.clickCell(row, column)
                self.play()
        except LostException:
            self.drawer.draw(self.board)
            print('You lost the game')
            return
        except ValueError as error:
            args = error.args
            print('The value for ' + args[1] + ' must be between 0 and ' + str(args[2]))
            self.play()

class Cell:
    STATUS_HIDDEN = 'hidden'
    STATUS_FLAGGED = 'flagged'
    STATUS_VISIBLE = 'visible'

    def __init__(self, x: int, y: int, has_mine: bool) -> None:
        self.x = x
        self.y = y
        self.status = self.STATUS_HIDDEN
        self.value = 0
        self.has_mine = has_mine
    
    def flag(self) -> None:
        if self.status == self.STATUS_FLAGGED:
            self.status = self.STATUS_HIDDEN
        elif self.status == self.STATUS_HIDDEN:
            self.status = self.STATUS_FLAGGED
    
    def click(self) -> bool:
        self.status = self.STATUS_VISIBLE

        if self.has_mine:
            return False
        return True

    def isVisible(self) -> bool:
        return self.status == self.STATUS_VISIBLE
    
    def isFlagged(self) -> bool:
        return self.status == self.STATUS_FLAGGED

class Board:
    def __init__(self, height: int, width: int, mines: int) -> None:
        self.height = height
        self.width = width
        self.mines = mines

        total_cells = self.height * self.width
        
        cells = []
        for i in range(self.height):
            cells.append([])
            for j in range(self.width):
                has_mine = False

                probability = 100 * mines / total_cells
                random_num = random.randint(0, 100)
                if random_num <= probability:
                    has_mine = True
                    mines -= 1
                
                total_cells -= 1
                
                cells[i].append(Cell(i, j, has_mine))
        
        self.cells = cells
    
    def flagCell(self, x: int, y: int) -> None:
        self.__checkInput(x,y)
        self.cells[x][y].flag()
    
    def neighboringMines(self, x: int, y: int) -> int:
        total_mines = 0

        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if i < 0 or j < 0 or i == self.width or j == self.height:
                    continue
                cell = self.cells[i][j]
                if cell.has_mine:
                    total_mines += 1
        
        return total_mines        
    
    def clickCell(self, x: int, y: int) -> None:
        self.__checkInput(x,y)

        cell = self.cells[x][y]
        clear_cell = cell.click()
        if False == clear_cell:
            raise LostException()
        
        cell.value = self.neighboringMines(x,y)
                    
        if cell.value == 0:
            for i in range(x-1, x+2):
                for j in range(y-1, y+2):

                    if i < 0 or j < 0 or i == self.width or j == self.height or self.cells[i][j].isVisible() or self.cells[i][j].isFlagged():
                        continue

                    self.clickCell(i,j)
    
    def __checkInput(self, x: int, y: int) -> None:
        if x < 0 or x > self.width:
            raise ValueError('OutOfRange', 'row', self.width)
        if y < 0 or y > self.height:
            raise ValueError('OutOfRange', 'column', self.height)



class Drawer:
    def draw(self, board: Board):
        for i in range(board.width + 2):
            row = ''
            for j in range(board.height + 2):
                if i == 0 or i == board.width + 1:
                    row += '__'
                    continue
                if j == 0 or j == board.height + 1:
                    row += '|'
                    continue
                if board.cells[i - 1][j - 1].isFlagged():
                    row += ' F'
                    continue
                if False == board.cells[i - 1][j - 1].isVisible():
                    row += ' &'
                    continue
                if board.cells[i - 1][j - 1].has_mine:
                    row += ' *'
                    continue
                row += ' ' + str(board.cells[i - 1][j - 1].value)

                
            print(row)

class LostException(Exception):
    pass

game = Game(Board(10, 10, 10))  
