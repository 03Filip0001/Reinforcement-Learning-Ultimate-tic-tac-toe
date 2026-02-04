from enum import Enum

class CellValues(Enum):
    EMPTY = 0
    X = 1
    O = -1

class Cell:
    def __init__(self):
        self.value = CellValues.EMPTY