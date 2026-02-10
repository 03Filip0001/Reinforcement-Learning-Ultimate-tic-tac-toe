import sys
import pygame
from src.cell import CellValues
from src.board import Board
from src.gameDisplay import GameDisplay

def main():
    board = Board()
    display = GameDisplay(board=board)
    
    winner = CellValues.EMPTY
    currentPlayer = CellValues.X
    nextBoardPos = None
    running = True
    print(board.getBoardList())
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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