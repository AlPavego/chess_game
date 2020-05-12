from figure import Figure


class King(Figure):
    def __init__(self, color, position):
        self.name = 'King'
        super(King, self).__init__(color, position)
        self.image = 'images/w_king.png' if self.color == 'w' else 'images/b_king.png'

    def possible_moves(self, board):
        # Возвращает возможные движения
        moves = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                place = self.pos[0] + i, self.pos[1] + j
                if place[0] > 7 or place[0] < 0 or place[1] > 7 or place[1] < 0:
                    continue
                cell = board[place[0]][place[1]]
                if not cell or self.is_enemy(cell):
                    moves.append(place)
        return moves
