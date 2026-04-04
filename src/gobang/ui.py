import pygame

class BoardUI:
    def __init__(self, screen, cell_size=40):
        self.screen = screen
        self.cell_size = cell_size
        
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.board_width = 14 * cell_size
        self.board_height = 14 * cell_size
        self.board_rect = pygame.Rect(0, 0, self.board_width, self.board_height)

        # 游戏内布局：左侧棋盘，右侧操作区
        self.board_margin_x = 20
        self.panel_gap = 20
        self.panel_width = 280
        self.start_x = self.board_margin_x
        self.start_y = (self.screen_height - self.board_height) // 2
        self.panel_rect = pygame.Rect(
            self.start_x + self.board_width + self.panel_gap,
            20,
            self.panel_width,
            self.screen_height - 40,
        )

        self.font_large = pygame.font.SysFont('simhei', 84) # 大号字体用于主菜单标题
        self.font_medium = pygame.font.SysFont('simhei', 48) # 中号字体用于小标题及主菜单按钮
        self.font_small = pygame.font.SysFont('simhei', 36) # 小号字体用于小按钮
        self.font_panel = pygame.font.SysFont('simhei', 28)
        
        # 游戏内操作按钮（放在右侧面板）
        btn_w = self.panel_width - 40
        btn_h = 50
        btn_x = self.panel_rect.x + 20
        btn_top = self.panel_rect.y + 182
        btn_gap = 12
        self.menu_btn_rect = pygame.Rect(btn_x, btn_top, btn_w, btn_h)
        self.undo_btn_rect = pygame.Rect(btn_x, btn_top + (btn_h + btn_gap) * 1, btn_w, btn_h)
        self.restart_btn_rect = pygame.Rect(btn_x, btn_top + (btn_h + btn_gap) * 2, btn_w, btn_h)
        self.win_quit_btn_rect = pygame.Rect(btn_x, btn_top + (btn_h + btn_gap) * 3, btn_w, btn_h)

        # 主菜单
        btn_width, btn_height = 250, 60
        self.pvp_btn_rect = pygame.Rect(
            (self.screen_width - btn_width) // 2, 
            self.screen_height // 2 - 80, 
            btn_width, 
            btn_height
        )
        self.pve_btn_rect = pygame.Rect(
            (self.screen_width - btn_width) // 2,
            self.screen_height // 2,
            btn_width,
            btn_height,
        )
        self.quit_btn_rect = pygame.Rect(
            (self.screen_width - btn_width) // 2, 
            self.screen_height // 2 + 80, 
            btn_width, 
            btn_height
        )
    
    def draw_main_menu(self):
        self.screen.fill((240, 217, 181))

        # 游戏标题
        title_text = "五子棋"
        title_surface = self.font_large.render(title_text, True, (0, 0, 0))
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 4 - 10))
        self.screen.blit(title_surface, title_rect)

        # 绘制按钮
        self.draw_button(self.pvp_btn_rect, "玩家对战", self.pvp_btn_rect.collidepoint(pygame.mouse.get_pos()), 1)
        self.draw_button(self.pve_btn_rect, "人机对战", self.pve_btn_rect.collidepoint(pygame.mouse.get_pos()), 1)
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

    def draw_game_panel(self, current_player, game_over, winner, vs_ai=False):
        # 右侧操作区背景
        pygame.draw.rect(self.screen, (205, 170, 120), self.panel_rect, border_radius=14)
        pygame.draw.rect(self.screen, (100, 80, 50), self.panel_rect, 2, border_radius=14)

        title_text = "人机对战" if vs_ai else "玩家对战"
        title_surface = self.font_medium.render(title_text, True, (40, 30, 20))
        title_rect = title_surface.get_rect(center=(self.panel_rect.centerx, self.panel_rect.y + 60))
        self.screen.blit(title_surface, title_rect)

        if game_over:
            info_text = f"玩家{'1' if winner == 1 else '2'}获胜"
        else:
            info_text = f"当前: 玩家{current_player}"

        info_surface = self.font_panel.render(info_text, True, (40, 30, 20))
        info_rect = info_surface.get_rect(center=(self.panel_rect.centerx, self.panel_rect.y + 120))
        self.screen.blit(info_surface, info_rect)

        if game_over:
            self.draw_victory_banner(winner, vs_ai)

        mouse_pos = pygame.mouse.get_pos()
        self.draw_button(self.menu_btn_rect, "返回主菜单", self.menu_btn_rect.collidepoint(mouse_pos), 2)
        self.draw_button(self.undo_btn_rect, "悔棋", self.undo_btn_rect.collidepoint(mouse_pos), 2)
        self.draw_button(self.restart_btn_rect, "重新开始", self.restart_btn_rect.collidepoint(mouse_pos), 2)
        self.draw_button(self.win_quit_btn_rect, "退出游戏", self.win_quit_btn_rect.collidepoint(mouse_pos), 2)

    def draw_victory_banner(self, winner, vs_ai=False):
        overlay = pygame.Surface((self.board_width, self.board_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 55))
        self.screen.blit(overlay, (self.start_x, self.start_y))

        banner_rect = pygame.Rect(self.start_x + 20, self.start_y + 20, self.board_width - 40, 130)
        pygame.draw.rect(self.screen, (255, 215, 0), banner_rect, border_radius=22)
        pygame.draw.rect(self.screen, (180, 40, 40), banner_rect, 6, border_radius=22)

        if vs_ai:
            title = "你赢了！" if winner == 1 else "AI 获胜"
            sub_title = "点击右侧按钮重新开始或退出"
        else:
            title = f"玩家{'1' if winner == 1 else '2'} 获胜！"
            sub_title = "点击右侧按钮重新开始或退出"

        title_surface = self.font_medium.render(title, True, (180, 30, 30) if winner == 1 else (40, 40, 40))
        title_rect = title_surface.get_rect(center=(banner_rect.centerx, banner_rect.centery - 18))
        self.screen.blit(title_surface, title_rect)

        sub_surface = self.font_panel.render(sub_title, True, (70, 50, 20))
        sub_rect = sub_surface.get_rect(center=(banner_rect.centerx, banner_rect.centery + 42))
        self.screen.blit(sub_surface, sub_rect)


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
        # 保留兼容接口：当前胜负信息由右侧面板显示
        pass
