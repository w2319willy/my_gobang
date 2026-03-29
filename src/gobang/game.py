import pygame
from src.gobang.logic import GameLogic
from src.gobang.ui import BoardUI

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((700, 700))
        pygame.display.set_caption("五子棋")
        
        # 初始化模块
        self.logic = GameLogic()
        self.ui = BoardUI(self.screen)
        self.game_state = 0 #主菜单逻辑 0主菜单；1游戏中
        self.running = True
        self.current_player = 1 # 1是黑棋
        self.game_over = False
        self.winner = None

        self.restart_btn_rect = pygame.Rect(250, 400, 200, 50)
        self.win_quit_btn_rect = pygame.Rect(250, 500, 200, 50)

    def reset_game(self):
        #重置游戏数据
        self.logic = GameLogic()
        self.current_player = 1
        self.game_over = False
        self.winner = None

    def run(self):
        while self.running:
            #根据状态绘制游戏画面
            if self.game_state == 0: #主菜单
                self.ui.draw_main_menu()

            elif self.game_state == 1:# 游戏中
                self.screen.fill((220, 179, 92)) # 画个木色背景
                self.ui.draw_grid()

                #重绘已经存在的棋子 (这一步很重要，否则棋子会消失)
                for r in range(15):
                    for c in range(15):
                        if self.logic.board[r][c] != 0:
                            self.ui.draw_stone(r, c, self.logic.board[r][c])
            
            if self.game_over:
                self.ui.draw_winner_ui(self.winner)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                 # 根据状态处理事件
                if self.game_state == 0:# 主菜单
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.ui.start_btn_rect.collidepoint(event.pos):
                            self.game_state = 1 # 切换到游戏中
                        elif self.ui.quit_btn_rect.collidepoint(event.pos):
                            self.running = False #退出游戏

                elif self.game_state == 1:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if not self.game_over:
                            # 处理点击，换算成坐标
                            mx, my = pygame.mouse.get_pos()
                            # 坐标换算逻辑
                            col = round((mx - self.ui.start_x) / self.ui.cell_size)
                            row = round((my - self.ui.start_y) / self.ui.cell_size)
                            
                            if 0 <= row < 15 and 0 <= col < 15:
                                if self.logic.board[row][col] == 0: # 如果是空地
                                    # 落子
                                    self.logic.board[row][col] = self.current_player
                                    self.ui.draw_stone(row, col, self.current_player)
                                    
                                    # 判断输赢
                                    if self.logic.check_win(row, col, self.current_player):
                                        self.game_over = True
                                        self.winner = self.current_player
                                    
                                    # 换人
                                    self.current_player = 2 if self.current_player == 1 else 1
                        else:
                            # 游戏结束时的点击逻辑 
                            # 检查是否点击了“重新开始”按钮
                            if self.restart_btn_rect.collidepoint(event.pos):
                                self.reset_game()
                            if self.win_quit_btn_rect.collidepoint(event.pos):
                                self.running = False
            
            pygame.display.flip()
        
        pygame.quit()