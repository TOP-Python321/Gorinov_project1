"""
Работа с данными игроков.
"""
import data
import game
import utils


def name_input() -> str:
    """
    Запрашивает и проверяет имя пользователя на соответствие шаблону. Если имя корректное то
     возвращает имя как объект str.
    :return: str - имя пользователя
    """
    while True:
        name = input(f' {data.MESSAGES["ввод имени"]}{data.PROMPT}')
        if data.NAME_PATTERN.fullmatch(name):
            return name
        print(f'{data.MESSAGES["некорректное имя"]}')


def get_players_name(flag: bool = False) -> None:
    """
    Запрашивает имя игрока. Если имени нет в базе игроков, то добавляет имя в базу игроков и обновляет файлы данных.
    :param flag: При передаче в качестве аргумента True меняет запустившего игру игрока на нового игрока.
    :return: None
    """
    name = name_input()

    if name not in data.players_db:
        data.players_db[name] = {'побед': 0, 'поражений': 0, 'ничьих': 0}
        utils.write_players()
        # !!!написать вывод помощи!!!
        # help.full()
    if flag:
        data.players = [name]
        data.authorized = [name]
    else:
        data.players += [name]
        data.authorized = data.players[0]


def get_bot_name(name: str) -> None:
    """
    Записывает бота как второго игрока.
    """
    if name not in data.players_db:
        data.players_db[name] = {'побед': 0, 'поражений': 0, 'ничьих': 0}
        utils.write_players()
    data.players += [name]


def update_stats(players: list[str]):
    if not players:
        for name in data.players:
            data.players_db[name]['ничьих'] += 1
    else:
        data.players_db[players[0]]['побед'] += 1
        data.players_db[players[1]]['поражений'] += 1
    # подготовка списка к следующей партии
    game.clear()


def turn_order(inp: str) -> None:
    """
    Принимает строку. Переворачивает список data.players, если введена не пустая строка.
    """
    if inp:
        data.players.reverse()


def player_search(player: str) -> bool:
    """
    Принимает имя игрока в виде объекта str. Возвращает TRUE если имя есть в списке data.saves_db,
    иначе возвращает Folse
    :return: bool
    """
    for elems in data.saves_db:
        for elem in elems:
            if player in elem:
                return bool(True)

    print(f'У игрока {player} нет загруженных партий')
    return bool(False)


def search_saves() -> list[tuple[str, str], dict]:
    """
    Запрашивае у игрока пртию, которую необходимо загрузить. Возвращает список из кортежа игроков и
    списка сделанных ходов.
    """
    list_saves = []
    count = 1
    for elem in data.saves_db:
        if data.authorized in elem:
            list_saves.append(elem)
            print(f'{count}. {elem}')
            count += 1

    if list_saves:
        while True:
            inp = input(f"{data.MESSAGES['номер партии']} {data.PROMPT}")
            try:
                inp = int(inp)
            except ValueError:
                pass
            else:
                if 1 <= inp <= count - 1:
                    return [save := list_saves[inp - 1], data.saves_db[save]]
