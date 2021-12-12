from board import Board


class ScoreScheme:
    def __init__(self, scheme, max_depth):
        self.scheme = scheme
        self.max_depth = max_depth
        print(self.max_depth, type(self.max_depth))

    def score(self, board: Board):
        return self.min_max(board) if self.scheme == 'min_max' else self.alpha_beta(board)

    def min_max(self, board: Board):
        pass

    def alpha_beta(self, board: Board):
        pass
