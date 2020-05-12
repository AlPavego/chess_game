from figure import Figure


class Rook(Figure):
    def __init__(self, color, position):
        self.name = 'Rook'
        super(Rook, self).__init__(color, position)
        self.image = 'images/w_rook.png' if self.color == 'w' else 'images/b_rook.png'

    def possible_moves(self, board):
        # Возвращает возможные движения
        return self.possible_straight_move(board)
