import pygame
from src.board import Board
from src.cell import CellValues

class GameDisplay:
    def __init__(self, board=None, window_size=900):
        pygame.init()
        self.window_size = window_size
        self.screen = pygame.display.set_mode((window_size, window_size))
        pygame.display.set_caption("Ultimate Tic-Tac-Toe")
        
        if board is None:
            raise Exception("Please provide board for display")
        
        self.board = board
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        
        # Size of one tic-tac-toe board
        self.big_cell_size = window_size // 3

        # Size of one cell in tic-tac-toe board
        self.small_cell_size = self.big_cell_size // 3
    
    def draw_grid(self):
        for row in range(3):
            for col in range(3):
                # Start coords for each cell
                start_x = col * self.big_cell_size
                start_y = row * self.big_cell_size
                
                for i in range(1, 3):
                    # Small vertical lines
                    lx = start_x + i * self.small_cell_size
                    pygame.draw.line(self.screen, self.GRAY, (lx, start_y), (lx, start_y + self.big_cell_size), 1)
                    
                    # Small horizontal lines
                    ly = start_y + i * self.small_cell_size
                    pygame.draw.line(self.screen, self.GRAY, (start_x, ly), (start_x + self.big_cell_size, ly), 1)

        # Vertical lines
        for i in range(1, 3):
            x = i * self.big_cell_size
            pygame.draw.line(self.screen, self.BLACK, (x, 0), (x, self.window_size), 3)
        
        # Horizontal lines
        for i in range(1, 3):
            y = i * self.big_cell_size
            pygame.draw.line(self.screen, self.BLACK, (0, y), (self.window_size, y), 3)

    def draw_symbols(self):
        for big_row in range(3):
            for big_col in range(3):
                ttt = self.board.board[big_row][big_col]
                
                for cell_row in range(3):
                    for cell_col in range(3):
                        cell_value = ttt.cells[cell_row][cell_col].getValue()
                        
                        if cell_value != CellValues.EMPTY:
                            # Pozicija na ekranu
                            x = big_col * self.big_cell_size + cell_col * self.small_cell_size + self.small_cell_size // 2
                            y = big_row * self.big_cell_size + cell_row * self.small_cell_size + self.small_cell_size // 2
                            
                            if cell_value == CellValues.X:
                                self.draw_x(x, y)
                            elif cell_value == CellValues.O:
                                self.draw_o(x, y)
    
    def draw_x(self, x, y):
        offset = self.small_cell_size // 4
        pygame.draw.line(self.screen, self.BLUE, 
                        (x - offset, y - offset), 
                        (x + offset, y + offset), 2)
        pygame.draw.line(self.screen, self.BLUE, 
                        (x + offset, y - offset), 
                        (x - offset, y + offset), 2)
    
    def draw_o(self, x, y):
        radius = self.small_cell_size // 4
        pygame.draw.circle(self.screen, self.RED, (x, y), radius, 2)
    
    def handle_click(self, pos, value):
        col = pos[0] // self.big_cell_size
        row = pos[1] // self.big_cell_size
        
        cell_col = (pos[0] % self.big_cell_size) // self.small_cell_size
        cell_row = (pos[1] % self.big_cell_size) // self.small_cell_size
        
        self.board.setValue([col, row], [cell_col, cell_row], value)
        self.board.checkWinner()

        if value == CellValues.X:
            return CellValues.O
        else:
            return CellValues.X
    
    def update(self):
        """Update display"""
        self.screen.fill(self.WHITE)
        self.draw_grid()
        self.draw_symbols()
        pygame.display.flip()
    
    def get_clock(self):
        return self.clock