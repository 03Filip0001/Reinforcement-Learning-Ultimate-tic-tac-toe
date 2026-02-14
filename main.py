import sys
import pygame
from src.cell import CellValues
from src.board import Board
from src.gameDisplay import GameDisplay

import pickle
from pathlib import Path

def main():
    temp_dir = Path("temp")
    temp_dir.mkdir(parents=True, exist_ok=True)

    board = Board()
    display = GameDisplay(board=board)
    
    winner = CellValues.EMPTY
    currentPlayer = CellValues.X
    nextBoardPos = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                print("Saved in temp/")
                with open("temp/data.json", "wb") as f:
                    pickle.dump(board, f)
                    
                with open("temp/currentPlayer.json", "wb") as f:
                    pickle.dump(currentPlayer, f)

                with open("temp/nextBoardPos.json", "wb") as f:
                    pickle.dump(nextBoardPos, f)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                print("Loaded from temp/")
                with open("temp/data.json", "rb") as f:
                    board = pickle.load(f)
                    
                with open("temp/currentPlayer.json", "rb") as f:
                    currentPlayer = pickle.load(f)

                with open("temp/nextBoardPos.json", "rb") as f:
                    nextBoardPos = pickle.load(f)

                display.changeBoard(board)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                boardPos, cellPos = display.handle_click(event.pos, currentPlayer)
                valid, nextBoardPos = board.play(boardPos, cellPos, nextBoardPos, currentPlayer)

                if valid:
                    if currentPlayer == CellValues.X:
                        currentPlayer = CellValues.O
                    else:
                        currentPlayer = CellValues.X
                
                winner = board.checkWinner()
                if winner is not CellValues.EMPTY:
                    running = False
        
        display.update(nextBoardPos)
        display.get_clock().tick(10)
    
    print("Winner of the game is " + winner.name)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()