from typing import Optional
import pygame
import pickle

from src.player import Player, PlayerType

from src.gameBase import GameBase
from src.XO.cell import CellValues
from src.XO.gameDisplay import GameDisplay

class Game:
    def __init__(self, modelPath: str, firstToPlay: int = 0, agentCount: int = 1, window_size: int = 1200):
        self.modelPath = modelPath
        
        self.game = GameBase()
        self.playerOne: Optional[Player] = None
        self.playerTwo: Optional[Player] = None
        
        self.window_size = window_size
        self.display = GameDisplay(self.game.getBoard(), self.window_size)
        self.FPS: int = 10
        
        self.clickedBoard:  int     = 0
        self.clickedCell:   tuple[int, int] = (0, 0)
        self.clicked:       bool    = False
                
        if agentCount != 2:
            self.playerOne = Player(CellValues.X, PlayerType.HUMAN)
        else:
            self.playerOne = Player(CellValues.X, PlayerType.AGENT, modelPath=self.modelPath)

        if agentCount == 1 or agentCount == 2:
            self.playerTwo = Player(CellValues.O, PlayerType.AGENT, modelPath=self.modelPath)
        else:
            self.playerTwo = Player(CellValues.O, PlayerType.HUMAN)
        
        assert self.playerOne is not None and self.playerTwo is not None
        player_one: Player = self.playerOne
        player_two: Player = self.playerTwo
        self.currentPlayer: Player = player_one if player_one.getPlayer() == self.game.getCurrentPlayer() else player_two
        
    def run(self):
        while self.game.getRunning():
            self.update()
            self.render()
            self.display.get_clock().tick(self.FPS)
        self.display.quit()
    
    def update(self):
        self.handleEvents()
        action = self.getAction()
        if action is None:
            return
        
        self.game.play(action[0], action[1], self.currentPlayer.getPlayer())
        if self.game.getLastValid():
            self.game.checkWinner()
            player_one: Player = self.playerOne if self.playerOne is not None else self.playerTwo
            player_two: Player = self.playerTwo if self.playerTwo is not None else self.playerOne
            new_player = player_one if player_one.getPlayer() == self.game.getCurrentPlayer() else player_two
            assert new_player is not None
            self.currentPlayer = new_player
    
    def render(self):
        self.display.update(self.game.getNextBoardPos())
    
    def getAction(self):
        action = None
        
        if self.currentPlayer.getType() == PlayerType.HUMAN \
            and self.clicked == True:
            action = (self.clickedBoard, self.clickedCell)
            self.clicked = False
        elif self.currentPlayer.getType() == PlayerType.AGENT:
            # Agent playing
            action = self.currentPlayer.play(self.game.getBoard(), self.currentPlayer.getPlayer(), self.game.getNextBoardPos())
        
        return action
    
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.setRunning(False)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.saveGame()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                self.loadGame()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.currentPlayer.getType() == PlayerType.HUMAN:
                    self.clickedBoard, self.clickedCell = self.display.handle_click(event.pos)
                    self.clicked = True
                    
    def saveGame(self):
        print("Saved in temp/")
        with open("temp/gameState.json", "wb") as f:
            gameState = [self.game.getBoard(), self.currentPlayer, self.game.getNextBoardPos()]
            pickle.dump(gameState, f)
                    
    def loadGame(self):
        print("Loaded from temp/")
        with open("temp/data.json", "rb") as f:
            gameState = pickle.load(f)
            self.currentPlayer = gameState[1]
            self.game.setPlayer(self.currentPlayer.getPlayer())            
            self.game.setNextBoardPos(gameState[2])
            
            self.display.changeBoard(self.game.getBoard())
            self.game.changeBoard(self.game.getBoard())
            
    def getWinner(self):
        return self.game.getWinner()