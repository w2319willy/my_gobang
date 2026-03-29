class GameLogic:
    def __init__(self, size=15):
        self.size = size
        # 0:空, 1:黑, 2:白
        self.board = [[0 for _ in range(size)] for _ in range(size)]

    def check_win(self, row, col, player):
        # 这里写判断输赢的算法
        # 检查横、竖、斜、反斜四个方向
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            count = 1 # 当前落子算1个
            # 向一个方向检查
            r, c = row + dr, col + dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player:
                count += 1
                r += dr
                c += dc
            # 向反方向检查
            r, c = row - dr, col - dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player:
                count += 1
                r -= dr
                c -= dc
            
            if count >= 5:
                return True
        return False