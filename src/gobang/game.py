import pygame
from src.gobang.ai import GobangAI
from src.gobang.logic import GameLogic
from src.gobang.ui import BoardUI

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((900, 700))
        pygame.display.set_caption("五子棋")
        
        # 初始化模块
        self.logic = GameLogic()
        self.ui = BoardUI(self.screen)
        self.ai = GobangAI(self.logic.size)
        self.game_state = 0 #主菜单逻辑 0主菜单；1游戏中
        self.running = True
        self.current_player = 1 # 1是黑棋
        self.game_over = False
        self.winner = None
        self.vs_ai = False
        self.ai_player = 2

    def undo_move(self):
        if self.vs_ai:
            # 人机模式下：若最后一步是AI，则回退两步；否则只回退一步
            if not self.logic.move_history:
                return

            last_player = self.logic.move_history[-1][2]
            self.logic.undo_last_move()
            if last_player == self.ai_player and self.logic.move_history:
                self.logic.undo_last_move()
            self.current_player = 1
            self.game_over = False
            self.winner = None
            return

        undone = self.logic.undo_last_move()
        if undone is None:
            return

        _, _, player = undone
        self.current_player = player
        self.game_over = False
        self.winner = None

    def start_game(self, vs_ai):
        self.vs_ai = vs_ai
        self.reset_game()
        self.game_state = 1

    def apply_move(self, row, col, player):
        if not self.logic.place_stone(row, col, player):
            return False

        if self.logic.check_win(row, col, player):
            self.game_over = True
            self.winner = player
            return True

        self.current_player = 2 if player == 1 else 1
        return True

    def try_ai_move(self):
        if self.game_over or not self.vs_ai or self.current_player != self.ai_player:
            return

        row, col = self.ai.choose_move(self.logic.board, self.ai_player)
        self.apply_move(row, col, self.ai_player)

    def reset_game(self):
        #重置游戏数据
        self.logic = GameLogic()
        self.current_player = 1
        self.game_over = False
        self.winner = None

    def return_to_main_menu(self):
        self.reset_game()
        self.vs_ai = False
        self.game_state = 0

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

                self.ui.draw_game_panel(self.current_player, self.game_over, self.winner, self.vs_ai)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                 # 根据状态处理事件
                if self.game_state == 0:# 主菜单
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.ui.pvp_btn_rect.collidepoint(event.pos):
                            self.start_game(vs_ai=False)
                        elif self.ui.pve_btn_rect.collidepoint(event.pos):
                            self.start_game(vs_ai=True)
                        elif self.ui.quit_btn_rect.collidepoint(event.pos):
                            self.running = False #退出游戏

                elif self.game_state == 1:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.ui.menu_btn_rect.collidepoint(event.pos):
                            self.return_to_main_menu()
                            continue

                        if self.ui.undo_btn_rect.collidepoint(event.pos):
                            self.undo_move()
                            continue

                        if self.ui.restart_btn_rect.collidepoint(event.pos):
                            self.reset_game()
                            continue

                        if self.ui.win_quit_btn_rect.collidepoint(event.pos):
                            self.running = False
                            continue

                        if not self.game_over:
                            # 处理点击，换算成坐标
                            mx, my = pygame.mouse.get_pos()
                            # 坐标换算逻辑
                            col = round((mx - self.ui.start_x) / self.ui.cell_size)
                            row = round((my - self.ui.start_y) / self.ui.cell_size)
                            
                            if 0 <= row < 15 and 0 <= col < 15:
                                # 人机模式下，只有玩家1可手动落子
                                if (not self.vs_ai) or self.current_player != self.ai_player:
                                    self.apply_move(row, col, self.current_player)

            if self.game_state == 1:
                self.try_ai_move()
            
            pygame.display.flip()
        
        pygame.quit()