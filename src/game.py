"""
Настройка партии и игровой процесс.
"""
# стандартная библиотека
from shutil import get_terminal_size
# проект
import data
import player
import utils


def get_human_turn() -> int | None:
    while True:
        turn = input(f"{data.MESSAGES['ход']}{data.PROMPT}")
        if not turn:
            return None
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
    for t in range(len(data.turns), data.all_cells):
        # добавил вывод игрового поля, т.к. при загрузке существующей партии неизвестно какие поля заняты без
        # вывода игрового поля
        if flag:
            print_board()
            # print(data.field.format(*(data.board | data.turns).values()))
            flag = False
        o = t % 2

        turn = get_human_turn()
        if turn is None:
            # сохранение незавершенной партии
            utils.save_game()
            data.players = [data.authorized]
            data.turns = {}
            return None
        data.turns[turn] = data.TOKENS[o]
        # print(data.field.format(*(data.board | data.turns).values()))
        print_board(o)
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
    Запрашивает режим игры. Если введена пустая строка добавляет бота как второго игрока, иначе запрашивает имя второго
    игрока.
    """
    inp = input(f"{data.MESSAGES['режим игры']}{data.PROMPT}")
    if inp:
        player.get_players_name()
    else:
        # !!!здесь будет добавление бота !!!
        print('игра с ботом')


def load(players: tuple[str, str], save: dict) -> None:
    """
    Перезаписывает переменные необходимые для игрового процесса принятыми аргументами.
    """
    data.players = list(players)
    data.turns = save['turns']
    utils.change_dim(save['dim'])


def print_board(right: bool = False) -> None:
    """
    Выводит в stdout игровое поле. При условии data.DEBUG = True выводит отладочные игровые поля.
    :param right: По умолчанию выравнивает игровое поле по левой стороне, иначе по правой стороне.
    :return: None
    """
    board = data.field.format(*(data.board | data.turns).values())
    if data.DEBUG:
        matr = bot.vectorization(data.debug_data.get('result'))
        cw = max(len(str(n)) for n in matr)
        matr = utils.field_template(cw).format(*matr)
        board = utils.concatenate_rows(board, matr)

    if right:
        terminal_width = get_terminal_size()[0] - 1
        margin = terminal_width - max(len(line) for line in board.split())
        margin = '\n'.join(' '*margin for _ in board.split())
        board = utils.concatenate_rows(margin, board, padding=0)

    print(board)


def clear() -> None:
    """
    Подготавливает переменные к следующей партии. Удаляет доигранную партию из data.saves_db, если она там есть.
    """
    data.saves_db.pop(tuple(data.players), None)
    data.players = [data.authorized]
    data.turns = {}
