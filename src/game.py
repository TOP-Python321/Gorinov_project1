"""
Настройка партии и игровой процесс.
"""
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


def game() -> list[str] | None:
    """Контроллер игрового процесса."""

    for t in range(len(data.turns), data.all_cells):
        o = t % 2

        turn = get_human_turn()
        if turn is None:
            utils.save_game()
            return None
        data.turns[turn] = data.TOKENS[o]
        print(data.field_template.format(*(data.field_coordinates | data.turns).values()))
        if (
                set(tuple(data.turns)[::2]) in data.winning_combinations or
                set(tuple(data.turns)[1::2]) in data.winning_combinations
        ):
            print(f'выиграл игрок {data.players[o]}')
            result_players = data.players[:]
            if data.players[o] != data.players[0]:
                result_players.reverse()
            return result_players
    else:
        # ничья
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
