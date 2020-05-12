import pygame
from pygame.locals import *
from board import ChessBoard
from figures.queen import Queen


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Шахматы')
        pygame.display.set_icon(pygame.image.load('images/icon.jpg'))
        self.screen = pygame.display.set_mode((860, 565))

        self.clock = pygame.time.Clock()
        self.board = ChessBoard()

        self.main_menu = pygame.image.load('images/main_menu.jpg')
        self.main_menu = pygame.transform.scale(self.main_menu, (860, 565))
        self.board_img = pygame.image.load('images/board.png')
        self.win_background = pygame.Surface((860, 565))
        self.poss_target = pygame.Surface((self.board.cell_size, self.board.cell_size))
        self.target_image = pygame.Surface((self.board.cell_size, self.board.cell_size))
        self.target_enemy_image = pygame.Surface((self.board.cell_size, self.board.cell_size))
        self.move_history = pygame.Surface((270, 310))

        self.win_background.set_alpha(150)
        self.poss_target.set_alpha(125)
        self.target_image.set_alpha(125)
        self.target_enemy_image.set_alpha(125)

        pygame.draw.rect(self.win_background, (255, 255, 255), self.win_background.get_rect())
        pygame.draw.rect(self.poss_target, (173, 255, 182), self.poss_target.get_rect())
        pygame.draw.rect(self.target_image, (173, 255, 255), self.target_image.get_rect())
        pygame.draw.rect(self.target_enemy_image, (255, 173, 173), self.target_enemy_image.get_rect())

        self.w_figures_captured_images = []
        self.b_figures_captured_images = []

        self.new_game = False
        self.pause = True
        self.winner = None
        
        self.target = None
        self.target_poss_moves = ()
        self.all_poss_moves = self.get_all_poss_moves()

        self.main_loop()

    def main_loop(self):
        running = True
        
        while running:
            self.draw_window()

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == MOUSEBUTTONUP and event.button == 1:
                    self.get_click()
            self.clock.tick(60)

    def draw_window(self):
        if not self.new_game:
            # Вывод главного меню
            self.draw_main_menu()
        else:
            # Вывод доски
            self.draw_board()
        if self.winner:
            # Вывод победного меню
            self.draw_win_menu()
        pygame.display.update()

    def reset(self):
        # Обнуление игры
        self.screen.fill((250, 232, 167))
        self.new_game = False
        self.pause = True
        self.winner = None
        self.figure_untarget()
        self.all_poss_moves = self.get_all_poss_moves()
        self.board.reset()
        self.draw_window()

    def draw_main_menu(self):
        # Главное меню
        new_game = pygame.Surface((400, 85))
        exit = pygame.Surface((250, 85))

        new_game.set_alpha(150)
        exit.set_alpha(150)
        # Фон для кнопок
        pygame.draw.rect(new_game, (105, 105, 105), new_game.get_rect())
        pygame.draw.rect(exit, (105, 105, 105), exit.get_rect())

        self.screen.blit(self.main_menu, (0, 0))
        self.screen.blit(new_game, (225, 210))
        self.screen.blit(exit, (305, 310))

        self.message_display('Новая игра', (425, 250), font_color=(255, 255, 255))
        self.message_display('Выход', (425, 350), font_color=(255, 255, 255))

        pygame.display.update()

    def draw_board(self):
        # Отрисовка всего на доске
        self.screen.fill((250, 232, 167))
        self.screen.blit(self.board_img, (0, 0))

        # Выделение фигуры
        if not self.pause:
            if self.target:
                self.screen.blit(self.target_image, self.get_coords(self.target.pos))
                # Выделение доступных для хода клеток
                if self.target_poss_moves:
                    for move in self.target_poss_moves:
                        # Если пустая
                        if self.board.field[move[0]][move[1]]:
                            self.screen.blit(self.target_enemy_image, self.get_coords(move))
                        # Если вражеская фигура
                        else:
                            self.screen.blit(self.target_image, self.get_coords(move))
            else:
                # Фигуры текущего игрока, которые могут ходить
                for cell in self.all_poss_moves.keys():
                    if self.all_poss_moves[cell]:
                        self.screen.blit(self.poss_target, self.get_coords(cell))

        # Отрисовка координатного поля на доске
        for i in range(8, 0, -1):
            x, y = self.get_coords((0, i - 1))
            self.message_display('%s' % i,
                                 (int(x - self.board.edge * 0.5), int(y + self.board.cell_size * 0.5)), 24)
            x, y = self.get_coords((i - 1, 7))
            self.message_display('%s' % self.get_cell_name((i - 1, 7)),
                                 (int(x + self.board.edge), int(y + self.board.cell_size * 1.25)), 24)

        # Отрисовка фигур
        for figure in self.board.alive_figures():
            figure_pos = self.get_coords(figure.pos)
            figure_img = pygame.image.load(figure.image)
            figure_img = pygame.transform.scale(figure_img, (50, 50))
            self.screen.blit(figure_img, (figure_pos[0] + 7, figure_pos[1] + 7))

        # Отрисовка бокового меню
        self.draw_side_menu()

    def draw_side_menu(self):
        # Боковое меню
        player = 'белых' if self.board.curr_player == 'w' else 'черных'
        history_list = self.board.move_history
        hist_y = 3
        b_x, b_y = 570, 5
        w_x, w_y = 570, 505

        self.move_history.fill((250, 232, 167))
        self.message_display('Ход: %s' % player, (710, 120), 38)

        # Отображение истории ходов
        for move in history_list if len(history_list) < 12 else history_list[-12:]:
            move = str(history_list.index(move) + 1) + '. ' + move
            self.message_display(move, (15, hist_y), 23, align_left=1)
            hist_y += 25

        # Вставка таблицы на основной экран
        self.screen.blit(self.move_history, (577, 160))
        pygame.draw.rect(self.screen, (0, 0, 0), (577, 160, 270, 310), 3)

        # Отображение побеждённых чёрных фигур
        i = 0
        for b_fig in self.b_figures_captured_images:
            # Если фигур становится больше 8, то отрисовка идёт в 2 ряда
            if i == 9:
                b_x = 570
                b_y += 30

            b_fig = pygame.image.load(b_fig)
            b_fig = pygame.transform.scale(b_fig, (25, 25))
            self.screen.blit(b_fig, (b_x, b_y))
            b_x += 30
            i += 1

        # Отображение побеждённых белых фигур
        i = 0
        for w_fig in self.w_figures_captured_images:
            # Если фигур становится больше 8, то отрисовка идёт в 2 ряда
            if i == 9:
                w_x = 570
                w_y += 30
            w_fig = pygame.image.load(w_fig)
            w_fig = pygame.transform.scale(w_fig, (25, 25))
            self.screen.blit(w_fig, (w_x, w_y))
            w_x += 30
            i += 1

    def draw_win_menu(self):
        # Победное меню
        yes = pygame.Surface((90, 75))
        no = pygame.Surface((90, 75))

        yes.set_alpha(100)
        no.set_alpha(100)
        # Фон под кнопки
        pygame.draw.rect(yes, (100, 100, 100), yes.get_rect())
        pygame.draw.rect(no, (100, 100, 100), no.get_rect())
        # Отрисовка фона
        self.screen.blit(self.win_background, (0, 0))
        self.screen.blit(yes, (255, 365))
        self.screen.blit(no, (455, 365))

        self.message_display('Шах и Мат!', (425, 130))
        self.message_display('%s победили!' % self.winner, (425, 230))
        self.message_display('Вернутся в главное меню?', (425, 330), 56)
        self.message_display('Да', (300, 400), 48)
        self.message_display('Нет', (500, 400), 48)

        pygame.display.update()

    def get_coords(self, cell):
        # Клетка в координаты
        return cell[0] * self.board.cell_size + self.board.edge,\
               cell[1] * self.board.cell_size + self.board.edge

    def get_cell(self, coords):
        # Координаты в клетку
        x, y = (coords[0] - self.board.edge) // self.board.cell_size, \
               (coords[1] - self.board.edge) // self.board.cell_size
        if 0 <= x <= 7 and 0 <= y <= 7:
            return x, y

    def get_cell_name(self, cell, for_history=0):
        # Возвращает название клетки в виде ЦИФРАБУКВА (пример: (1,3) => 'B3')
        conversions = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
        if for_history:
            return str(conversions[cell[0]]) + str(cell[1] + 1)
        return str(conversions[cell[0]])

    def get_click(self):
        x, y = pygame.mouse.get_pos()
        # Обработка клика мыши
        # Получение клетки из координат
        cell = self.get_cell((x, y))
        # Если не пауза
        if not self.pause:
            if cell:
                # Фигура на клетке. Нужна для смены фокуса на другую союзную фигуру без повторного клика по текущей.
                cell_figure = self.board.figure_at(cell)
                # Если фигура не выбрана:
                if not self.target:
                    # Фокус на данную клетку
                    if self.is_curr_player_figure_at(cell):
                        self.figure_target(cell)
                # Если фигура уже выбрана:
                else:
                    # Убирает фокус при повторном нажатии
                    if cell == self.target.pos:
                        self.figure_untarget()
                    # Меняет фокус на другую союзную фигуру
                    elif cell_figure and cell_figure.color == self.board.curr_player:
                        self.figure_target(cell)
                    # Если клетка находится в доступных шагах:
                    elif cell in self.target_poss_moves:
                        # Является ли фигура королём
                        if self.target.name == 'King' and cell in self.board.castle_moves_for_player():
                            # Castle that king
                            self.add_move(self.target.pos, cell)
                            self.board.castle_king(self.target, cell)
                        else:
                            # Движение фигуры
                            self.add_move(self.target.pos, cell)
                            self.move_figure(self.target, cell)
                            # Повышение пешки
                            if self.target.name == 'Pawn' and (cell[1] == 0 or cell[1] == 7):
                                self.board.field[cell[0]][cell[1]] = None
                                self.board.field[cell[0]][cell[1]] = Queen(
                                    self.board.curr_player, cell)

                        # Снятие фокуса
                        self.figure_untarget()
                        # Смена игрока
                        self.change_player()
                        # Проверка на шах и мат, и обновление списка со всеми возможными ходами
                        self.all_poss_moves = self.get_all_poss_moves()
                        checkmate = True
                        for figures_pos in self.all_poss_moves:
                            if len(self.all_poss_moves[figures_pos]) != 0:
                                checkmate = False
                        # Если шах и мат:
                        if checkmate:
                            # Определение победителя
                            self.winner = 'Белые' if self.board.curr_player == 'b' else 'Чёрные'
                            self.pause = True
                            self.draw_board()
                            self.draw_win_menu()
        # Иначе переключение на победное/главное меню
        else:
            # Если есть победитель, то переключение на победное меню
            if self.winner:
                if 365 <= y <= 440:
                    # Если "да", то происходит сброс и возврат в гланое меню
                    if 255 <= x <= 345:
                        self.reset()
                    # Если "нет", то выход из игры
                    elif 455 <= x <= 545:
                        quit()
                    else:
                        pass
            # Иначе главное меню
            else:
                # Если "Новая игра"
                if 225 <= x <= 625 and 210 <= y <= 295:
                    self.new_game = True
                    self.pause = False
                # Если "Выход"
                elif 305 <= x <= 555 and 310 <= y <= 395:
                    quit()

    def get_target_poss_moves(self):
        # Получить возможные ходы
        return self.all_poss_moves[self.target.pos]

    def get_all_poss_moves(self):
        # Получить все возожные ходы для игрока
        moves = {}
        figures = self.board.curr_player_figures()
        for figure in figures:
            f_moves = self.board.possible_moves_for(figure)
            moves[figure.pos] = self.board.is_player_in_check(figure, f_moves)
        return moves

    def figure_target(self, cell):
        # Фокус на фигуру
        self.target = self.board.figure_at(cell)
        self.target_poss_moves = self.get_target_poss_moves()

    def figure_untarget(self):
        # Снятие фокуса
        self.target = None
        self.target_poss_moves = None

    def is_curr_player_figure_at(self, cell):
        # Является ли фигура фигруой текущего игрока
        for figure in self.board.curr_player_figures():
            if cell == figure.pos:
                return True

    def change_player(self):
        # Смена игрока
        self.board.curr_player = 'w' if self.board.curr_player == 'b' else 'b'

    def move_figure(self, figure, cell):
        # Движение фигуры и захват срезанной фигуры, если есть
        figure_captured = self.board.move_figure(figure, cell)
        if figure_captured:
            self.figure_was_captured(figure_captured)

    def add_move(self, pos_1, pos_2):
        # Добавление хода в историю
        name = 'Б: ' if self.board.curr_player == 'w' else 'Ч: '
        move = name + self.get_cell_name(pos_1, for_history=1) + ' => ' + self.get_cell_name(pos_2, for_history=1)
        self.board.move_history.append(move)

    def figure_was_captured(self, figure):
        # Получегие изображения захваченной фигуры
        if figure.color == 'w':
            self.w_figures_captured_images.append(figure.image)
        else:
            self.b_figures_captured_images.append(figure.image)

    def message_display(self, text, coords, font_size=68, font_color=(0, 0, 0), align_left=0):
        # Отображение сообщения
        font_dir = pygame.font.match_font('verdana')
        text_font = pygame.font.Font(font_dir, font_size)
        text_surface = text_font.render(text, True, font_color)
        if not align_left:
            text_rect = text_surface.get_rect()
            text_rect.center = (coords)
            self.screen.blit(text_surface, text_rect)
        else:
            self.move_history.blit(text_surface, coords)


if __name__ == '__main__':
    Game()