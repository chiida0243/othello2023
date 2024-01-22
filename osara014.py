import copy

class OthelloAI:
    def __init__(self, player, depth=3):
        self.player = player
        self.depth = depth

    def evaluate_board(self, board):
        score = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] == self.player:
                    if (i == 0 or i == 7) and (j == 0 or j == 7):
                        score += 10
                    elif (i == 0 or i == 7 or j == 0 or j == 7):
                        score += 5
                    else:
                        score += 1
                elif board[i][j] != ' ':
                    score -= 1
        return score

    def minmax(self, board, depth, maximizing_player):
        if depth == 0 or self.game_over(board):
            return self.evaluate_board(board)

        legal_moves = self.get_legal_moves(board)

        if maximizing_player:
            max_eval = float('-inf')
            for move in legal_moves:
                new_board = copy.deepcopy(board)
                self.make_move(new_board, move[0], move[1])
                eval = self.minmax(new_board, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                new_board = copy.deepcopy(board)
                self.make_move(new_board, move[0], move[1])
                eval = self.minmax(new_board, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def get_legal_moves(self, board):
        legal_moves = []
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(board, i, j):
                    legal_moves.append((i, j))
        return legal_moves

    def is_valid_move(self, board, row, col):
        if board[row][col] == ' ':
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                pieces_to_flip = []
                while 0 <= r < 8 and 0 <= c < 8 and board[r][c] != ' ' and board[r][c] != self.player:
                    pieces_to_flip.append((r, c))
                    r += dr
                    c += dc
                if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == self.player and pieces_to_flip:
                    return True
        return False

    def make_move(self, board, row, col):
        if self.is_valid_move(board, row, col):
            board[row][col] = self.player
            self.flip_pieces(board, row, col)

    def flip_pieces(self, board, row, col):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            pieces_to_flip = []
            while 0 <= r < 8 and 0 <= c < 8 and board[r][c] != ' ' and board[r][c] != self.player:
                pieces_to_flip.append((r, c))
                r += dr
                c += dc
            if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == self.player and pieces_to_flip:
                for piece in pieces_to_flip:
                    board[piece[0]][piece[1]] = self.player

    def game_over(self, board):
        for i in range(8):
            for j in range(8):
                if board[i][j] == ' ':
                    return False
        return True

    def get_best_move(self, board):
        legal_moves = self.get_legal_moves(board)

