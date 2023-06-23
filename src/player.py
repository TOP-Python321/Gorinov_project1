"""
Работа с данными игроков.
"""
import data
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


def get_players_name() -> None:
    """
    Запрашивает имя игрока. Если имени нет в базе игроков, то добавляет имя в базу игроков и обновляет файлы данных.
    :return: None
    """
    name = name_input()

    if name not in data.players_db:
        data.players_db[name] = {'побед': 0, 'поражений': 0, 'ничьих': 0}
        utils.write_players()
        # !!!написать вывод помощи!!!
        # help.full()
    data.players += [name]


def update_stats(players: list[str]):
    if not players:
        for name in data.players:
            data.players_db[name]['ничьих'] += 1
    else:
        data.players_db[players[0]]['побед'] += 1
        data.players_db[players[1]]['поражений'] += 1
