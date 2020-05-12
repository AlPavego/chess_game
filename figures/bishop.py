from figure import Figure


class Bishop(Figure):
    def __init__(self, color, position):
        self.name = 'Bishop'
        super(Bishop, self).__init__(color, position)
        self.image = 'images/w_bishop.png' if self.color == 'w' else 'images/b_bishop.png'

    def possible_moves(self, board):
        # Возвращает возможные движения
        return self.possible_diag_move(board)
