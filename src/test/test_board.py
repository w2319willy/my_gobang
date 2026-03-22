import pygame
import sys
# 导入模块
from src.gobang.board import BoardUI 

def main():
    pygame.init()
    screen = pygame.display.set_mode((700, 700))
    pygame.display.set_caption("测试棋盘")
    clock = pygame.time.Clock()

    my_board = BoardUI(screen, cell_size=40)

    running = True
    while running:
        #处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #清空屏幕 (画背景色)
        screen.fill((220, 179, 92))
        #调用 board.py 里的画图函数
        my_board.draw_grid()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()