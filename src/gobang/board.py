import pygame

class BoardUI:
    def __init__(self, screen, cell_size=40):
        self.screen = screen
        self.cell_size = cell_size
        self.margin = 30 # 棋盘边缘留白

    def draw_grid(self):
        # 画15x15的线
        for i in range(15):
            # 横线
            start_pos = (self.margin, self.margin + i * self.cell_size)
            end_pos = (self.margin + 14 * self.cell_size, self.margin + i * self.cell_size)
            pygame.draw.line(self.screen, (0, 0, 0), start_pos, end_pos)
            # 竖线
            start_pos = (self.margin + i * self.cell_size, self.margin)
            end_pos = (self.margin + i * self.cell_size, self.margin + 14 * self.cell_size)
            pygame.draw.line(self.screen, (0, 0, 0), start_pos, end_pos)