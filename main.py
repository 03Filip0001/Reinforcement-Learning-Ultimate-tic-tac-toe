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
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                currentPlayer = display.handle_click(event.pos, currentPlayer)
                
                winner = board.checkWinner()
                if winner is not CellValues.EMPTY:
                    running = False
        
        display.update()
        display.get_clock().tick(10)
    
    print("Winner of the game is " + winner.name)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()