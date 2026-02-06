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