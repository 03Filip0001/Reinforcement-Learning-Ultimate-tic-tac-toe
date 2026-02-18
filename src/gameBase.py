from src.XO.board import Board
from src.XO.cell import CellValues

class GameBase:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.board: Board = Board()
        
        self.winner = CellValues.EMPTY
        self.valid = False
        self.nextBoardPos = None
        
        self.currentPlayer = CellValues.X
        self.running = True

    def play(self, bigCoords, smallCoords, sign: CellValues):
        self.valid, self.nextBoardPos = self.board.play(bigCoords, smallCoords, self.nextBoardPos, sign)
    
        if self.valid:
            if self.currentPlayer == CellValues.X:
                self.currentPlayer = CellValues.O
            else:
                self.currentPlayer = CellValues.X
    
    def checkWinner(self):
        self.winner = self.board.checkWinner()
        
        if self.winner is not CellValues.EMPTY:
            self.running = False
            
        return not self.running
            
            
    def getWinner(self):
        return self.winner
    
    def getBoard(self):
        return self.board
    
    def getNextBoardPos(self):
        return self.nextBoardPos
    
    def setNextBoardPos(self, boardPos):
        self.nextBoardPos = boardPos
    
    def getLastValid(self):
        return self.valid
    
    def getRunning(self):
        return self.running
    
    def setRunning(self):
        self.running = False
    
    def getWinner(self):
        return self.winner
    
    def getCurrentPlayer(self):
        return self.currentPlayer
    
    def setPlayer(self, player):
        self.currentPlayer = player
    
    def changeBoard(self, board: Board):
        self.board = board