from figure import Figure


class Queen(Figure):
    def __init__(self, color, position):
        self.name = 'Queen'
        super(Queen, self).__init__(color, position)
        self.image = 'images/w_queen.png' if self.color == 'w' else 'images/b_queen.png'

    def possible_moves(self, board):
        # Возвращает возможные движения
        return self.possible_diag_move(board) + self.possible_straight_move(board)
