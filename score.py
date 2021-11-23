from board import Board


class ScoreScheme:
    def __init__(self, scheme):
        self.scheme = scheme

    def score(self, board: Board):
        return self.min_max(board) if self.scheme == 'min_max' else self.exp_max(board)

    def min_max(self, board: Board):
        pass

    def exp_max(self, board: Board):
        pass
