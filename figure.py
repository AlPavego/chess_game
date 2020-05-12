class Figure:
    def __init__(self, color, pos):
        self.color = color.lower()
        self.en_color = 'b' if self.color == 'w' else 'w'
        self.pos = pos
        self.direction = 1 if color == 'w' else -1
        self.moved = False
        self.poss_moves = []

    def move(self, pos):
        # Меняет координаты фигуры
        self.pos = pos

    def possible_moves(self, board):
        return []

    def is_enemy(self, figure):
        # Возврщает является ли фигура врагом текущей
        return figure.color == self.en_color

    def possible_straight_move(self, board):
        # Возвращает возможные движения по прямой
        moves = []
        curr_pos = self.pos[0], self.pos[1] + 1
        while curr_pos[1] <= 7:
            figure = board[curr_pos[0]][curr_pos[1]]
            if not figure:
                moves.append(curr_pos)
            elif self.is_enemy(figure):
                moves.append(curr_pos)
                break
            else:
                break

            curr_pos = curr_pos[0], curr_pos[1] + 1

        curr_pos = self.pos[0], self.pos[1] - 1
        while curr_pos[1] >= 0:
            figure = board[curr_pos[0]][curr_pos[1]]
            if not figure:
                moves.append(curr_pos)
            elif self.is_enemy(figure):
                moves.append(curr_pos)
                break
            else:
                break

            curr_pos = curr_pos[0], curr_pos[1] - 1

        curr_pos = self.pos[0] + 1, self.pos[1]
        while curr_pos[0] <= 7:
            figure = board[curr_pos[0]][curr_pos[1]]
            if not figure:
                moves.append(curr_pos)
            elif self.is_enemy(figure):
                moves.append(curr_pos)
                break
            else:
                break

            curr_pos = curr_pos[0] + 1, curr_pos[1]

        curr_pos = self.pos[0] - 1, self.pos[1]
        while curr_pos[0] >= 0:
            figure = board[curr_pos[0]][curr_pos[1]]
            if not figure:
                moves.append(curr_pos)
            elif self.is_enemy(figure):
                moves.append(curr_pos)
                break
            else:
                break

            curr_pos = curr_pos[0] - 1, curr_pos[1]

        return moves

    def possible_diag_move(self, board):
        # Возвращает возможные движения по диагонали
        moves = []
        curr_pos = self.pos[0] + 1, self.pos[1] + 1
        while curr_pos[1] <= 7 and curr_pos[0] <= 7:
            figure = board[curr_pos[0]][curr_pos[1]]
            if not figure:
                moves.append(curr_pos)
            elif self.is_enemy(figure):
                moves.append(curr_pos)
                break
            else:
                break

            curr_pos = curr_pos[0] + 1, curr_pos[1] + 1

        curr_pos = self.pos[0] + 1, self.pos[1] - 1
        while curr_pos[1] >= 0 and curr_pos[0] <= 7:
            figure = board[curr_pos[0]][curr_pos[1]]
            if not figure:
                moves.append(curr_pos)
            elif self.is_enemy(figure):
                moves.append(curr_pos)
                break
            else:
                break

            curr_pos = curr_pos[0] + 1, curr_pos[1] - 1

        curr_pos = self.pos[0] - 1, self.pos[1] + 1
        while curr_pos[0] >= 0 and curr_pos[1] <= 7:
            figure = board[curr_pos[0]][curr_pos[1]]
            if not figure:
                moves.append(curr_pos)
            elif self.is_enemy(figure):
                moves.append(curr_pos)
                break
            else:
                break

            curr_pos = curr_pos[0] - 1, curr_pos[1] + 1

        curr_pos = self.pos[0] - 1, self.pos[1] - 1
        while curr_pos[1] >= 0 and curr_pos[0] >= 0:
            figure = board[curr_pos[0]][curr_pos[1]]
            if not figure:
                moves.append(curr_pos)
            elif self.is_enemy(figure):
                moves.append(curr_pos)
                break
            else:
                break

            curr_pos = curr_pos[0] - 1, curr_pos[1] - 1

        return moves
