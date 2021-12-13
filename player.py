from board import Board


class Player:
    def __init__(self, player_type):
        self.player_type = player_type

    def update_board(self, board: Board, col=-1):
        pass


class Human(Player):
    def __init__(self, val=False):
        super().__init__(val)

    def update_board(self, board: Board, col=-1):
        board.set_piece(col, self.player_type)


class Computer(Player):
    def __init__(self, val=True):
        super().__init__(val)

    def update_board(self, board: Board, col=-1):
        board.set_piece(col, self.player_type)
