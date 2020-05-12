from figure import Figure


class Pawn(Figure):
    def __init__(self, color, position):
        self.name = 'Pawn'
        super(Pawn, self).__init__(color, position)
        self.image = 'images/w_pawn.png' if color == 'w' else 'images/b_pawn.png'

    def possible_moves(self, board):
        # Возвращает возможные движения
        moves = []
        # Если спереди ничего нет
        if not self.figure_in_front(board):
            moves.append((self.pos[0], self.pos[1] + self.direction))
            # Если первый ход для пешки, то может двигаться на 2 клетки
            if (not self.moved) and (not board[self.pos[0]][self.pos[1] + 2 * self.direction]):
                moves.append((self.pos[0], self.pos[1] + 2 * self.direction))
        # Если есть враг по правой диагонали
        if self.pos[0] < 7:
            right_diagonal = board[self.pos[0] + 1][self.pos[1] + self.direction]
            if right_diagonal and self.is_enemy(right_diagonal):
                moves.append(right_diagonal.pos)
        # Если есть враг по левой диагонали
        if self.pos[0] > 0:
            left_diagonal = board[self.pos[0] - 1][self.pos[1] + self.direction]
            if left_diagonal and self.is_enemy(left_diagonal):
                moves.append(left_diagonal.pos)
        return moves

    def figure_in_front(self, board):
        # Возвращает занята ли клетка спереди
        return board[self.pos[0]][self.pos[1] + self.direction]
