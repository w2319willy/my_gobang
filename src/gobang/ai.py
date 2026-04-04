import random


class GobangAI:
	def __init__(self, board_size=15):
		self.board_size = board_size

	def choose_move(self, board, ai_player=2):
		opponent = 1 if ai_player == 2 else 2

		# 有直接赢棋点先下
		winning_move = self.find_winning_move(board, ai_player)
		if winning_move is not None:
			return winning_move

		# 对方出现三连时，优先堵住其中一端，避免对手轻松冲成四连或五连。
		open_three_block = self.find_open_three_block_move(board, opponent)
		if open_three_block is not None:
			return open_three_block

		# 对手有直接赢棋点先堵
		block_move = self.find_winning_move(board, opponent)
		if block_move is not None:
			return block_move

		# 否则在候选点里做评分（靠近中心 + 邻近已有棋子）并选最高分
		candidates = self.get_candidate_moves(board)
		if not candidates:
			center = self.board_size // 2
			return center, center

		best_score = None
		best_moves = []
		for row, col in candidates:
			score = self.evaluate_position(board, row, col)
			if best_score is None or score > best_score:
				best_score = score
				best_moves = [(row, col)]
			elif score == best_score:
				best_moves.append((row, col))

		return random.choice(best_moves)

	def find_winning_move(self, board, player):
		# 枚举候选点，临时落子后判断这一手是否能形成五连。
		for row, col in self.get_candidate_moves(board):
			board[row][col] = player
			is_win = self.check_win(board, row, col, player)
			board[row][col] = 0
			if is_win:
				return row, col
		return None

	def find_open_three_block_move(self, board, player):
		# 扫描所有方向上的“0 + 3子 + 0”结构，命中后只堵住其中一端。
		directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
		for row in range(self.board_size):
			for col in range(self.board_size):
				for dr, dc in directions:
					end_row = row + dr * 4
					end_col = col + dc * 4
					if not self.in_bounds(end_row, end_col):
						continue

					cells = []
					for step in range(5):
						r = row + dr * step
						c = col + dc * step
						cells.append(board[r][c])

					if cells[0] == 0 and cells[4] == 0 and cells[1] == player and cells[2] == player and cells[3] == player:
						# 先堵一端，优先堵靠近中心的一侧。
						open_end_1 = (row, col)
						open_end_2 = (end_row, end_col)
						return self.choose_better_block_end(board, open_end_1, open_end_2)
		return None

	def get_candidate_moves(self, board):
		# 只考虑已有棋子周围的空位，减少无意义的全盘搜索。
		stones = []
		for r in range(self.board_size):
			for c in range(self.board_size):
				if board[r][c] != 0:
					stones.append((r, c))

		if not stones:
			center = self.board_size // 2
			return [(center, center)]

		candidates = set()
		for r, c in stones:
			for dr in range(-2, 3):
				for dc in range(-2, 3):
					nr, nc = r + dr, c + dc
					if 0 <= nr < self.board_size and 0 <= nc < self.board_size and board[nr][nc] == 0:
						candidates.add((nr, nc))

		return list(candidates)

	def evaluate_position(self, board, row, col):
		# 位置评分由两部分组成：越接近中心越高，周围有子也会加分。
		center = self.board_size // 2
		center_score = (self.board_size - abs(row - center) - abs(col - center))

		neighbor_score = 0
		for dr in range(-1, 2):
			for dc in range(-1, 2):
				if dr == 0 and dc == 0:
					continue
				nr, nc = row + dr, col + dc
				if 0 <= nr < self.board_size and 0 <= nc < self.board_size and board[nr][nc] != 0:
					neighbor_score += 2

		return center_score + neighbor_score

	def choose_better_block_end(self, board, pos1, pos2):
		# 两个端点都能堵时，优先选择更靠近中心、周围影响更大的那个。
		score1 = self.evaluate_position(board, pos1[0], pos1[1])
		score2 = self.evaluate_position(board, pos2[0], pos2[1])
		return pos1 if score1 >= score2 else pos2

	def in_bounds(self, row, col):
		return 0 <= row < self.board_size and 0 <= col < self.board_size

	def check_win(self, board, row, col, player):
		# 检查横、竖、主对角线、副对角线四个方向是否连成五子。
		directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
		for dr, dc in directions:
			count = 1

			r, c = row + dr, col + dc
			while 0 <= r < self.board_size and 0 <= c < self.board_size and board[r][c] == player:
				count += 1
				r += dr
				c += dc

			r, c = row - dr, col - dc
			while 0 <= r < self.board_size and 0 <= c < self.board_size and board[r][c] == player:
				count += 1
				r -= dr
				c -= dc

			if count >= 5:
				return True
		return False
