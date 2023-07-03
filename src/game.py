"""
Настройка партии и игровой процесс.
"""
# стандартная библиотека
from shutil import get_terminal_size
# проект
import data
import player
import utils
import bot


def get_human_turn(flag) -> int | None:
    """Запрашивает координаты игрового поля. При получении 'help' вызывает функцию print_board()"""
    while True:
        turn = input(f"{data.MESSAGES['ход']}{data.PROMPT}")
        if not turn:
            return None
        if turn == 'help':
            print_board(right=flag, switch=True)
        try:
            turn = int(turn)
        except ValueError:
            pass
        else:
            if 1 <= turn <= data.all_cells:
                if turn not in data.turns:
                    return turn


def game(flag: bool = False) -> list[str] | None:
    """Контроллер игрового процесса."""
    data.field = utils.field_template()
    data.winning_combinations = utils.counts_combinations(data.dim)
    data.dict_board = dict(zip(range(1, data.all_cells + 1), range(1, data.all_cells + 1)))
    data.START_MATRICES = (
        bot.calc_sm_cross(),
        bot.calc_sm_zero()
    )
    for t in range(len(data.turns), data.all_cells):
        # добавил вывод игрового поля, т.к. при загрузке существующей партии неизвестно какие поля заняты без
        # вывода игрового поля
        if flag:
            print_board()
            flag = False
        o = t % 2
        if data.players[o] == 'БотЛ':
            turn = bot.easy_mode()
        elif data.players[o] == 'БотС':
            turn = bot.hard_mode()
        else:
            turn = get_human_turn(o)
        if turn is None:
            # сохранение незавершенной партии
            utils.save_game()
            data.players = [data.authorized]
            data.turns = {}
            return None
        data.turns[turn] = data.TOKENS[o]
        print_board(o)
        # !!!добавить условие для проверки!!!
        for elem in data.winning_combinations:
            if (elem <= set(tuple(data.turns)[::2]) or
                elem <= set(tuple(data.turns)[1::2])
            ):
                print(f"{data.MESSAGES['выигрыш']} {data.players[o]}")
                copy_players = data.players[:]
                if data.players[o] != data.players[0]:
                    copy_players.reverse()
                return copy_players
    else:
        # ничья
        print(f"{data.MESSAGES['ничья']}")
        return []


def game_mode() -> None:
    """
    Запрашивает режим игры. При получении пустой строки вызывает функцию запроса имени  второго игрока
    (player.get_players_name()),
    при получении '1' добавляет легкого бота вторым игроком,
    при получении '2' добавляет сложного бота вторым игроком.
    """
    while True:
        inp = input(f"{data.MESSAGES['режим игры']}{data.PROMPT}")
        if not inp:
            player.get_players_name()
            break
        elif inp == '1':
            player.get_bot_name('БотЛ')
            break
        elif inp == '2':
            player.get_bot_name('БотС')
            break


def load(players: tuple[str, str], save: dict) -> None:
    """
    Перезаписывает переменные необходимые для игрового процесса принятыми аргументами.
    """
    data.players = list(players)
    data.turns = save['turns']
    utils.change_dim(save['dim'])


def print_board(right: bool = False, switch: bool = False) -> None:
    """
    Выводит в stdout игровое поле. При условии data.DEBUG = True выводит отладочные игровые поля.
    :param right: По умолчанию выравнивает игровое поле по левой стороне, иначе по правой стороне.
    :param switch: При передаче True - выводит на печать игровое поле с координатами и занятыми ячейками.
                    По умолчинию выводит игровое поле.
    :return: None
    """
    if switch:
        data_width = max(len(str(n)) for n in (data.dict_board | data.turns).values())
        board = utils.field_template(data_width).format(*(f'{n:>{data_width}}' for n in
                                                          (data.dict_board | data.turns).values()))
    else:
        board = data.field.format(*(data.board | data.turns).values())

    # добавил проверку, если первым ходил не бот выходила ошибка
    if data.DEBUG and data.players[right] == 'БотС':
        matr = bot.vectorization(data.debug_data.get('empty'))
        cw = max(len(str(n)) for n in matr)
        matr = utils.field_template(cw).format(*matr)
        board = utils.concatenate_rows(board, matr, padding=8)

    if right:
        # условие для вывода отладочного поля справа для бота
        if data.DEBUG:
            terminal_width = get_terminal_size()[0] - 1
            margin = terminal_width - max(len(line) for line in board.split('\n'))
            margin = '\n'.join(' ' * margin for _ in board.split('\n'))
            board = utils.concatenate_rows(margin, board)
        else:
            terminal_width = get_terminal_size()[0] - 1
            margin = terminal_width - max(len(line) for line in board.split())
            margin = '\n'.join(' '*margin for _ in board.split())
            board = utils.concatenate_rows(margin, board)

    print(board)


def clear() -> None:
    """
    Подготавливает переменные к следующей партии. Удаляет доигранную партию из data.saves_db, если она там есть.
    """
    data.saves_db.pop(tuple(data.players), None)
    data.players = [data.authorized]
    data.turns = {}
