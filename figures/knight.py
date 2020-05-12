from figure import Figure


class Knight(Figure):
    def __init__(self, color, position):
        self.name = 'Knight'
        super(Knight, self).__init__(color, position)
        self.image = 'images/w_knight.png' if self.color == 'w' else 'images/b_knight.png'

    def possible_moves(self, board):
        # Возвращает возможные движения
        moves = []
        poss_moves = ((1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1))
        for move in poss_moves:
            pos = self.pos[0] + move[0], self.pos[1] + move[1]
            if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1] > 7:
                continue
            figure = board[pos[0]][pos[1]]
            if not figure or self.is_enemy(figure):
                moves.append(pos)
        return moves
