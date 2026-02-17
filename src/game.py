import pygame
import pickle

from src.player import Player, PlayerType

from src.XO.cell import CellValues
from src.XO.board import Board
from src.XO.gameDisplay import GameDisplay

class Game:
    def __init__(self, firstToPlay: int = 0, agentCount: int = 1, window_size: int = 1200):
        self.playerOne = None
        self.playerTwo = None
        
        self.board: Board = Board()
        self.window_size = window_size
        self.display = GameDisplay(self.board, self.window_size)
        self.FPS: int = 10
        
        self.winner = None
        
        self.nextBoardPos           = None
        
        self.clickedBoard:  int     = 0
        self.clickedCell:   int     = 0
        self.clicked:       bool    = False
        
        self.running = True
        
        if agentCount != 2:
            self.playerOne = Player(CellValues.X, PlayerType.HUMAN)
        else:
            self.playerOne = Player(CellValues.X, PlayerType.AGENT)

        if agentCount == 1 or agentCount == 2:
            self.playerTwo = Player(CellValues.O, PlayerType.AGENT)
        else:
            self.playerTwo = Player(CellValues.O, PlayerType.HUMAN)
                
        self.currentPlayer: Player = self.playerOne
        
    def run(self):
        while self.running:
            self.update()
            self.render()
            self.display.get_clock().tick(self.FPS)
    
    def update(self):
        self.handleEvents()
        action = self.getAction()
        if action is None:
            return
        
        valid, self.nextBoardPos = self.board.play(action[0], action[1], self.nextBoardPos, self.currentPlayer.getPlayer())
        if valid:
            self.winner = self.board.checkWinner()
            
            if self.winner is not CellValues.EMPTY:
                self.running = False
            else:
                if self.currentPlayer == self.playerOne:
                    self.currentPlayer = self.playerTwo
                else:
                    self.currentPlayer = self.playerOne
    
    def render(self):
        self.display.update(self.nextBoardPos)
    
    def getAction(self):
        action = None
        
        if self.currentPlayer.getType() == PlayerType.HUMAN \
            and self.clicked == True:
            action = (self.clickedBoard, self.clickedCell)
            self.clicked = False
        else:
            # Agent playing
            action = self.currentPlayer.play()
        
        return action
    
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.saveGame()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                self.loadGame()
                self.display.changeBoard(self.board)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.currentPlayer.getType() == PlayerType.HUMAN:
                    self.clickedBoard, self.clickedCell = self.display.handle_click(event.pos)
                    self.clicked = True
                    
    def saveGame(self):
        print("Saved in temp/")
        with open("temp/gameState.json", "wb") as f:
            gameState = [self.board, self.currentPlayer, self.nextBoardPos]
            pickle.dump(gameState, f)
                    
    def loadGame(self):
        print("Loaded from temp/")
        with open("temp/data.json", "rb") as f:
            gameState = pickle.load(f)
            self.board = gameState[0]
            self.currentPlayer = gameState[1]
            self.nextBoardPos = gameState[2]