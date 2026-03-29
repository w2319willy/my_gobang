import pygame

class BoardUI:
    def __init__(self, screen, cell_size=40):
        self.screen = screen
        self.cell_size = cell_size
        
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.board_width = 14 * cell_size
        self.board_height = 14 * cell_size

        # 计算棋盘左上角的起始坐标 (x, y)，使其居中
        self.start_x = (self.screen_width - self.board_width) // 2
        self.start_y = (self.screen_height - self.board_height) // 2

        self.font_large = pygame.font.SysFont('simhei', 72) # 大号字体用于主菜单标题
        self.font_medium = pygame.font.SysFont('simhei', 48) # 中号字体用于小标题及主菜单按钮
        self.font_small = pygame.font.SysFont('simhei', 36) # 小号字体用于小按钮
        
        #胜利界面
        self.restart_btn_rect = pygame.Rect(250, 400, 200, 50)
        self.win_quit_btn_rect = pygame.Rect(250, 500, 200, 50)

        #主菜单
        btn_width, btn_height = 250, 60
        #开始按钮
        self.start_btn_rect = pygame.Rect(
            (self.screen_width - btn_width) // 2, 
            self.screen_height // 2 - 40, 
            btn_width, 
            btn_height
        )
        # 退出按钮
        self.quit_btn_rect = pygame.Rect(
            (self.screen_width - btn_width) // 2, 
            self.screen_height // 2 + 40, 
            btn_width, 
            btn_height
        )
    
    def draw_main_menu(self):
        self.screen.fill((240, 217, 181))

        # 游戏标题
        title_text = "五子棋"
        title_surface = self.font_large.render(title_text, True, (0, 0, 0))
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 3))
        self.screen.blit(title_surface, title_rect)

        # 绘制按钮
        self.draw_button(self.start_btn_rect, "开始游戏", self.start_btn_rect.collidepoint(pygame.mouse.get_pos()), 1)
        self.draw_button(self.quit_btn_rect, "退出游戏", self.quit_btn_rect.collidepoint(pygame.mouse.get_pos()), 1)

    def draw_button(self, rect, text, hover, size):
        if size == 1: #主菜单
            # 按钮颜色
            bg_color = (200, 150, 100) if hover else (220, 180, 120)
            text_color = (255, 255, 255)
            
            # 绘制圆角矩形
            pygame.draw.rect(self.screen, bg_color, rect, border_radius=15)
            # 绘制边框
            pygame.draw.rect(self.screen, (100, 80, 50), rect, 2, border_radius=15)

            # 绘制文字
            text_surface = self.font_medium.render(text, True, text_color)
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)
        
        elif size == 2: 
            # 按钮颜色
            bg_color = (100, 100, 100) if hover else (60, 60, 60)
            text_color = (255, 255, 255)
            
            # 绘制圆角矩形
            pygame.draw.rect(self.screen, bg_color, rect, border_radius=10)
            # 绘制边框
            pygame.draw.rect(self.screen, (200, 200, 200), rect, 2, border_radius=10)

            # 绘制文字
            text_surface = self.font_small.render(text, True, text_color)
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)


    def draw_grid(self):
        # 画15x15的线
        for i in range(15):
            # 横线
            start_pos = (self.start_x, self.start_y + i * self.cell_size)
            end_pos = (self.start_x + 14 * self.cell_size, self.start_y + i * self.cell_size)
            pygame.draw.line(self.screen, (0, 0, 0), start_pos, end_pos)
            # 竖线
            start_pos = (self.start_x + i * self.cell_size, self.start_y)
            end_pos = (self.start_x + i * self.cell_size, self.start_y + 14 * self.cell_size)
            pygame.draw.line(self.screen, (0, 0, 0), start_pos, end_pos)

    def draw_stone(self, row, col, player):
        # 计算圆心坐标
        cx = self.start_x + col * self.cell_size
        cy = self.start_y + row * self.cell_size
            
        color = (0, 0, 0) if player == 1 else (255, 255, 255) # 黑棋或白棋
        # 画棋子
        pygame.draw.circle(self.screen, color, (cx, cy), self.cell_size // 2 - 2)

    def draw_winner_ui(self, winner):
        #绘制胜利界面和按钮
        # 半透明遮罩
        overlay = pygame.Surface((700, 700))
        overlay.set_alpha(180) 
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # 胜利文字
        winner_text = f"Player {'1' if winner == 1 else '2'} 获胜!"
        text_surface = self.font_medium.render(winner_text, True, (255, 215, 0))
        text_rect = text_surface.get_rect(center=(350, 300))
        self.screen.blit(text_surface, text_rect)
        
        '''
        # 绘制按钮背景
        # 检测鼠标是否悬停在按钮上，如果是，颜色变亮
        mouse_pos = pygame.mouse.get_pos()
        btn_color = (60, 60, 60) # 默认深灰
        if self.restart_btn_rect.collidepoint(mouse_pos) or self.win_quit_btn_rect.collidepoint(mouse_pos):
            btn_color = (100, 100, 100) # 悬停亮灰
            
        pygame.draw.rect(self.screen, btn_color, self.restart_btn_rect, border_radius=10)
        pygame.draw.rect(self.screen, (200, 200, 200), self.restart_btn_rect, 2, border_radius=10)
        pygame.draw.rect(self.screen, btn_color, self.win_quit_btn_rect, border_radius=10)
        pygame.draw.rect(self.screen, (200, 200, 200), self.win_quit_btn_rect, 2, border_radius=10)

        
        # 绘制按钮文字
        btn_text_1 = "重新开始"
        btn_surface_1 = self.font_small.render(btn_text_1, True, (255, 255, 255))
        btn_text_rect_1 = btn_surface_1.get_rect(center=self.restart_btn_rect.center)
        self.screen.blit(btn_surface_1, btn_text_rect_1)

        btn_text_2 = "退出游戏"
        btn_surface_2 = self.font_small.render(btn_text_2, True, (255, 255, 255))
        btn_text_rect_2 = btn_surface_2.get_rect(center=self.win_quit_btn_rect.center)
        self.screen.blit(btn_surface_2, btn_text_rect_2)
        '''
        #绘制按钮
        self.draw_button(self.restart_btn_rect, "重新开始", self.restart_btn_rect.collidepoint(pygame.mouse.get_pos()), 2)
        self.draw_button(self.win_quit_btn_rect, "退出游戏", self.win_quit_btn_rect.collidepoint(pygame.mouse.get_pos()), 2)
