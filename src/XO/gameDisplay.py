import pygame
from src.XO.board import Board
from src.XO.cell import CellValues

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
        self.OVERLAY_GRAY = (128, 128, 128)
        
        # Size of one tic-tac-toe board
        self.big_cell_size = window_size // 3

        # Size of one cell in tic-tac-toe board
        self.small_cell_size = self.big_cell_size // 3

    def changeBoard(self, board):
        self.board = board
    
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
        
        return ((col, row), (cell_col, cell_row))
    
    def draw_transparent_rect(self, big_col, big_row, alpha=100):
        """
        Crta polu-providni sivi kvadrat preko jednog velikog polja.
        alpha: 0 (potpuno providno) do 255 (potpuno neprovidno).
        """
        s = pygame.Surface((self.big_cell_size, self.big_cell_size))  # Kreiraj površinu veličine jednog velikog polja
        s.set_alpha(alpha)                # Podesi transparentnost
        s.fill(self.OVERLAY_GRAY)         # Oboj u sivo
        
        x = big_col * self.big_cell_size
        y = big_row * self.big_cell_size
        self.screen.blit(s, (x, y))       # "Zalepi" na glavnu površinu

    def draw_big_x(self, big_col, big_row):
        """Crta veliko X preko celog polja"""
        center_x = big_col * self.big_cell_size + self.big_cell_size // 2
        center_y = big_row * self.big_cell_size + self.big_cell_size // 2
        offset = self.big_cell_size // 3 # Malo veći offset da ne udara u ivice
        
        pygame.draw.line(self.screen, self.BLUE, 
                        (center_x - offset, center_y - offset), 
                        (center_x + offset, center_y + offset), 10) # Deblja linija
        pygame.draw.line(self.screen, self.BLUE, 
                        (center_x + offset, center_y - offset), 
                        (center_x - offset, center_y + offset), 10)

    def draw_big_o(self, big_col, big_row):
        """Crta veliko O preko celog polja"""
        center_x = big_col * self.big_cell_size + self.big_cell_size // 2
        center_y = big_row * self.big_cell_size + self.big_cell_size // 2
        radius = self.big_cell_size // 3
        
        pygame.draw.circle(self.screen, self.RED, (center_x, center_y), radius, 10) # Deblja linija
    
    def update(self, activeBoard):
        """Update display"""
        self.screen.fill(self.WHITE)
        self.draw_grid()
        self.draw_symbols()

        if activeBoard is not None:
            active_col, active_row = activeBoard
            for row in range(3):
                for col in range(3):
                    if (col, row) != (active_col, active_row):
                         self.draw_transparent_rect(col, row, alpha=100)

        # 2. ISCRTAVANJE POBEDNIKA I ZAVRŠENIH POLJA
        for row in range(3):
            for col in range(3):
                winner = self.board.board[row][col].checkWinner()
                
                if winner != CellValues.EMPTY and winner is not None:
                    # Prvo posivi malo jače da se istakne da je gotovo
                    self.draw_transparent_rect(col, row, alpha=150)
                    
                    # Onda nacrtaj veliki simbol
                    if winner == CellValues.X:
                        self.draw_big_x(col, row)
                    elif winner == CellValues.O:
                        self.draw_big_o(col, row)

        pygame.display.flip()
    
    def get_clock(self):
        return self.clock