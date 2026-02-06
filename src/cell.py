from enum import Enum

class CellValues(Enum):
    EMPTY = 0
    DRAW = -2
    X = 1
    O = -1

class Cell:
    def __init__(self):
        self.value = CellValues.EMPTY

    def __repr__(self):
        if self.value == CellValues.EMPTY:
            return " "
        elif self.value == CellValues.X:
            return "X"
        elif self.value == CellValues.O:
            return "O"
        else:
            raise Exception("Unknown cell value!")
        
    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value