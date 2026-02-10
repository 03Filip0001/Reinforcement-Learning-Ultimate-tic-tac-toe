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

    def play(self, bigCoords, smallCoords, validBoard, player):
        bigX, bigY = bigCoords
        smallX, smallY = smallCoords
      
        valid = False
        nextBigCoords = None
        if self.checkEmpty(bigCoords, smallCoords) and \
            (bigCoords == validBoard or validBoard == None) and \
            (self.board[bigY][bigX].checkWinner() == CellValues.EMPTY):

            valid = True
            self.setValue(bigCoords, smallCoords, player)
            nextBigCoords = smallCoords
            tttWinner = self.board[smallY][smallX].checkWinner()
            if tttWinner == CellValues.X or tttWinner == CellValues.O:
                nextBigCoords = None
        else:
            nextBigCoords = validBoard 

        return (valid, nextBigCoords)
    
    def checkEmpty(self, bigCoords, smallCoords):
        bigX, bigY = bigCoords
        smallX, smallY = smallCoords

        bigCell = self.board[bigY][bigX]
        smallCell = bigCell.cells[smallY][smallX]

        if smallCell.value == CellValues.EMPTY:
            return True
        else:
            return False

    def checkWinner(self):
        temp = 0
        if self.winner == CellValues.EMPTY:
            for row in range(3):
                for col in range(3):
                    if self.board[row][col].checkWinner() != CellValues.EMPTY:
                        temp += 1
            # DRAW
            if temp == 9:
                self.winner = CellValues.DRAW
            
            # Somebody won ?
            else:
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