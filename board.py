from figures.bishop import Bishop
from figures.king import King
from figures.knight import Knight
from figures.pawn import Pawn
from figures.queen import Queen
from figures.rook import Rook


class ChessBoard:
    def __init__(self):
        self.edge = 30
        self.cell_size = 63
        self.field = [[None for _ in range(8)] for _ in range(8)]
        for i in range(8):
            self.field[i][1] = Pawn('w', (i, 1))
            self.field[i][6] = Pawn('b', (i, 6))

        self.field[0][7] = Rook('b', (0, 7))
        self.field[7][7] = Rook('b', (7, 7))
        self.field[1][7] = Knight('b', (1, 7))
        self.field[6][7] = Knight('b', (6, 7))
        self.field[2][7] = Bishop('b', (2, 7))
        self.field[5][7] = Bishop('b', (5, 7))
        self.field[4][7] = King('b', (4, 7))
        self.field[3][7] = Queen('b', (3, 7))

        self.field[0][0] = Rook('w', (0, 0))
        self.field[7][0] = Rook('w', (7, 0))
        self.field[1][0] = Knight('w', (1, 0))
        self.field[6][0] = Knight('w', (6, 0))
        self.field[2][0] = Bishop('w', (2, 0))
        self.field[5][0] = Bishop('w', (5, 0))
        self.field[4][0] = King('w', (4, 0))
        self.field[3][0] = Queen('w', (3, 0))

        self.field_copy = self.field.copy()
        self.curr_player = 'w'
        self.move_history = []

    def reset(self):
        # Сброс доски
        self.field = self.field_copy
        self.curr_player = 'w'
        self.move_history = []

    def alive_figures(self):
        # Возвращает все живые фигуры на поле
        figures = []
        for i in range(8):
            for j in range(8):
                if self.field[i][j]:
                    figures.append(self.field[i][j])
        return figures

    def curr_player_figures(self):
        # Возвращает все живые фигуры текущего игрока
        figures = []
        for figure in self.alive_figures():
            if figure.color == self.curr_player:
                figures.append(figure)
        return figures

    def type_figures_of_player(self, figure_name, player_color):
        # Возврщает все фигуры данного типа, данного игрока
        figures = []
        for x in self.field:
            for cell in x:
                if cell and cell.name == figure_name and cell.color == player_color:
                    figures.append(cell)
        return figures

    def possible_moves_for(self, figure):
        # Возможные движения для фигуры с учётом Короля
        if figure.name != 'King':
            return figure.possible_moves(self.field)
        else:
            return figure.possible_moves(self.field) + self.castle_moves_for_player()

    def figure_at(self, cell):
        # Возвращает фигуру на клетке cell
        return self.field[cell[0]][cell[1]]

    def move_figure(self, figure, cell):
        # Двигает фигуру и изменяет её параметр moved на True
        pos = figure.pos
        figure_to_take = self.field[cell[0]][cell[1]]
        figure.move(cell)
        self.field[cell[0]][cell[1]] = figure
        self.field[pos[0]][pos[1]] = None
        if not figure.moved:
            figure.moved = True

        if figure_to_take:
            return figure_to_take
        return None

    def non_permanent_move(self, figure, cell):
        # Ход без изменения параметра moved. Нужен для шахов\шах и матов.
        pos = figure.pos
        figure.move(cell)
        self.field[cell[0]][cell[1]] = figure
        self.field[pos[0]][pos[1]] = None

    def castle_moves_for_player(self):
        # Возвращает движения с рокировкой
        castles = []
        king = self.type_figures_of_player('King', self.curr_player)[0]
        y = 0 if self.curr_player == 'w' else 7
        f = self.field
        # Проверяет двигались ли Король и Ладья
        if f[0][y] and not f[0][y].moved and f[4][y] and not f[4][y].moved:
            # Проверяет есть ли фигуры между Ладьёй и Королём
            if all(not f[x][y] for x in range(1, 4)):
                if not self.check_king(king, self.field):
                    castles.append((2, y))

        if f[7][y] and not f[7][y].moved and f[4][y] and not f[4][y].moved:
            if all(not f[x][y] for x in range(5, 7)):
                if not self.check_king(king, self.field):
                    castles.append((6, y))

        # Симулирует оба движения и проверяет игрока на шах
        for move in castles:
            self.non_permanent_castle_king(king, move)
            if self.check_king(king, self.field):
                castles.remove(move)
            # Отменяет рокировку
            self.uncastle_king(king)

        return castles

    def castle_king(self, king, king_pos):
        """Принимает фигуру Короля и одну из 4 позиций для рокировки. Двигает Короля и соответствующую ему ладью"""
        # NEW_KING_POS = (2, 0), (6, 0), (2, 7), (6, 7)
        corresponding_rook = {(2, 0): (0, 0), (6, 0): (7, 0), (2, 7): (0, 7), (6, 7): (7, 7)}
        corresponding_rook_move = {(2, 0): (3, 0), (6, 0): (5, 0), (2, 7): (3, 7), (6, 7): (5, 7)}
        rook_pos = corresponding_rook[king_pos]
        rook = self.field[rook_pos[0]][rook_pos[1]]
        self.move_figure(king, king_pos)
        self.move_figure(rook, corresponding_rook_move[king_pos])

    def uncastle_king(self, king):
        """Отменяет рокировку"""
        corresponding_rook = {(2, 0): (3, 0), (6, 0): (5, 0), (2, 7): (3, 7), (6, 7): (5, 7)}
        corresponding_rook_move = {(2, 0): (0, 0), (6, 0): (7, 0), (2, 7): (0, 7), (6, 7): (7, 7)}
        rook_pos = corresponding_rook[king.pos]
        rook = self.field[rook_pos[0]][rook_pos[1]]
        self.non_permanent_move(rook, corresponding_rook_move[king.pos])
        self.non_permanent_move(king, (4, king.pos[1]))

    def non_permanent_castle_king(self, king, king_pos):
        """Принимает фигуру Короля и одну из 4 позиций для рокировки. Двигает Короля и соответствующую ему ладью.
         Не меняет параметр фигуры moved"""
        # NEW_KING_POS = (2, 0), (6, 0), (2, 7), (6, 7)
        corresponding_rook = {(2, 0): (0, 0), (6, 0): (7, 0), (2, 7): (0, 7), (6, 7): (7, 7)}
        corresponding_rook_move = {(2, 0): (3, 0), (6, 0): (5, 0), (2, 7): (3, 7), (6, 7): (5, 7)}
        rook_pos = corresponding_rook[king_pos]
        rook = self.field[rook_pos[0]][rook_pos[1]]
        self.non_permanent_move(king, king_pos)
        self.non_permanent_move(rook, corresponding_rook_move[king_pos])

    def check_king(self, king, f):
        # Возвращает True если Король находится в шахе
        # Проверка есть ли Слон или Королева на диагональном пути Короля
        for c in king.possible_diag_move(f):
            if f[c[0]][c[1]] and f[c[0]][c[1]].name in ['Bishop', 'Queen']:
                return True

        # Проверка есть ли Ладья или Королева на прямом пути Короля
        for c in king.possible_straight_move(f):
            if f[c[0]][c[1]] and f[c[0]][c[1]].name in ['Rook', 'Queen']:
                return True

        # Проверка есть ли на пути короля другой Король
        for c in king.possible_moves(f):
            if f[c[0]][c[1]] and f[c[0]][c[1]].name == 'King':
                return True

        # Проверка на вражеских Коней
        for c in [(1, 2), (2, 1), (-1, 2), (-2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]:
            pos = king.pos[0] + c[0], king.pos[1] + c[1]
            if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1] > 7:
                continue
            if f[pos[0]][pos[1]] and f[pos[0]][pos[1]].name == 'Knight' \
                    and f[pos[0]][pos[1]].color != self.curr_player:
                return True

        # Проверка на пешки
        y_dir = 1 if self.curr_player == 'w' else -1
        # Проверка диагоналей
        l_diag = king.pos[0] - 1, king.pos[1] + y_dir
        r_diag = king.pos[0] + 1, king.pos[1] + y_dir

        if l_diag[0] >= 0:
            if f[l_diag[0]][l_diag[1]] and f[l_diag[0]][l_diag[1]].name == 'Pawn' \
                    and f[l_diag[0]][l_diag[1]].color != self.curr_player:
                return True
        if r_diag[0] <= 7:
            if f[r_diag[0]][r_diag[1]] and f[r_diag[0]][r_diag[1]].name == 'Pawn' \
                    and f[r_diag[0]][r_diag[1]].color != self.curr_player:
                return True

    def is_player_in_check(self, figure, moves):
        # Возвращает список движений, которые не приведут игрока к шаху
        king = self.type_figures_of_player('King', self.curr_player)[0]
        b = self.field
        figure_original_pos = figure.pos

        poss_moves = []

        for move in moves:
            # Move figure to new move
            figure_at_move_pos = self.field[move[0]][move[1]]
            self.non_permanent_move(figure, move)

            if not self.check_king(king, b):
                poss_moves.append(move)

            # Move figure back to original position
            self.non_permanent_move(figure, figure_original_pos)
            self.field[move[0]][move[1]] = figure_at_move_pos

        return poss_moves
