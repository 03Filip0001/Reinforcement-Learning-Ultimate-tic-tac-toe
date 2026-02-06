from src.ttt import TTT
from src.cell import CellValues

class Board:
    def __init__(self):
        self.board = []
        for _ in range(3):
            temp = []
            for _ in range(3):
                temp.append(TTT())

            self.board.append(temp)

        self.winner = CellValues.EMPTY

    def setValue(self, tttCoords, cellCoords, value):
        self.board[tttCoords[1]][tttCoords[0]].setCell(cellCoords, value)

    def getBoardList(self):
        ret = []
        for bigCellRow in self.board:
            bcr = []
            for bigCell in bigCellRow:
                bc = []
                for smallCellRow in bigCell.cells:
                    scr = []
                    for smallCell in smallCellRow:
                        scr.append(smallCell.value.value)
                    bc.append(scr)
                bcr.append(bc)
            ret.append(bcr)
        return ret

    def play(self, big_coords, small_coords, player):
        bigX, bigY = big_coords
        smallX, smallY = small_coords
      
        valid = False
        nextBigCoords = small_coords

        return (valid, nextBigCoords, player)
    
    def checkEmpty(self, big_coords, small_coords):
        bigX, bigY = big_coords
        smallX, smallY = small_coords

        bigCell = self.board[bigY][bigX]
        smallCell = bigCell.cells[smallY][smallX]

        if smallCell.value == CellValues.EMPTY:
            return True
        else:
            return False

    def checkWinner(self):
        if self.winner == CellValues.EMPTY:
            
            # Horizontal winner
            for i in range(3):
                if self.board[i][0].checkWinner() == self.board[i][1].checkWinner() and self.board[i][1].checkWinner() == self.board[i][2].checkWinner():
                    if self.board[i][0].checkWinner() == CellValues.X:
                        self.winner = CellValues.X
                    elif self.board[i][0].checkWinner() == CellValues.O:
                        self.winner = CellValues.O

            # Vertical winner
            for i in range(3):
                if self.board[0][i].checkWinner() == self.board[1][i].checkWinner() and self.board[1][i].checkWinner() == self.board[2][i].checkWinner():
                    if self.board[0][i].checkWinner() == CellValues.X:
                        self.winner = CellValues.X
                    elif self.board[0][i].checkWinner() == CellValues.O:
                        self.winner = CellValues.O

            # Diagonal win 1
            if self.board[0][0].checkWinner() == self.board[1][1].checkWinner() and self.board[1][1].checkWinner() == self.board[2][2].checkWinner():
                if self.board[1][1].checkWinner() == CellValues.X:
                    self.winner = CellValues.X
                elif self.board[1][1].checkWinner() == CellValues.O:
                    self.winner = CellValues.O

            # Diagonal win 2
            if self.board[0][2].checkWinner() == self.board[1][1].checkWinner() and self.board[1][1].checkWinner() == self.board[2][0].checkWinner():
                if self.board[1][1].checkWinner() == CellValues.X:
                    self.winner = CellValues.X
                elif self.board[1][1].checkWinner() == CellValues.O:
                    self.winner = CellValues.O

        return self.winner