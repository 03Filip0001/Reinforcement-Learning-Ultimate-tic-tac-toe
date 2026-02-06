from src.cell import Cell, CellValues

class TTT:
    def __init__(self):
        self.cells = []
        self.winner = CellValues.EMPTY

        for _ in range(3):
            temp = []
            for _ in range(3):
                temp.append(Cell())
            self.cells.append(temp)

    def __repr__(self):
        repr = "\n"
        for i in range(3):
            for j in range(3):
                repr += self.cells[i][j].__repr__()
                if j != 2:
                    repr += "|"

            if i != 2:
                repr += "\n-----\n"

        return repr
    
    def printWinner(self):
        if self.winner is CellValues.EMPTY:
            return "There is no winner yet !"
        else:
            return "Winner is player " + self.winner.name

    
    def setCell(self, coords, value):
        self.cells[coords[1]][coords[0]].setValue(value)

    def checkWinner(self):
        if self.winner is CellValues.EMPTY:
            
            # Horizontal win
            for i in range (3):
                if self.cells[i][0].getValue() == self.cells[i][1].getValue() and self.cells[i][1].getValue() == self.cells[i][2].getValue():
                    if self.cells[i][0].getValue() == CellValues.X:
                        self.winner = CellValues.X
                    elif self.cells[i][0].getValue() == CellValues.O:
                        self.winner = CellValues.O

            # Vertical win
            for i in range (3):
                if self.cells[0][i].getValue() == self.cells[1][i].getValue() and self.cells[1][i].getValue() == self.cells[2][i].getValue():
                    if self.cells[0][i].getValue() == CellValues.X:
                        self.winner = CellValues.X
                    elif self.cells[0][i].getValue() == CellValues.O:
                        self.winner = CellValues.O

            # Diagonal win 1
            if self.cells[0][0].getValue() == self.cells[1][1].getValue() and self.cells[1][1].getValue() == self.cells[2][2].getValue():
                if self.cells[1][1].getValue() == CellValues.X:
                    self.winner = CellValues.X
                elif self.cells[1][1].getValue() == CellValues.O:
                    self.winner = CellValues.O

            # Diagonal win 2
            if self.cells[0][2].getValue() == self.cells[1][1].getValue() and self.cells[1][1].getValue() == self.cells[2][0].getValue():
                if self.cells[1][1].getValue() == CellValues.X:
                    self.winner = CellValues.X
                elif self.cells[1][1].getValue() == CellValues.O:
                    self.winner = CellValues.O

        return self.winner