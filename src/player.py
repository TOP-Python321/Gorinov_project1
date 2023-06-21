"""
Работа с данными игроков.
"""
import data
from utils import write_players

def name_input() -> str:
    while True:
        name = input(f' {data.MESSAGES["ввод имени"]}{data.PROMPT}')
        if data.NAME_PATTERN.fullmatch(name):
            return name
        print(f'{data.MESSAGES["некорректное имя"]}')

def get_players_name() -> None:
    """"""
    name = name_input()

    if name not in data.players_db:
        data.players_db[name] = {'побед': 0, 'поражений': 0, 'ничьих': 0}
        # !!!написать функцию!!!
        write_players()
        # !!!написать вывод помощи!!!
        # help.full()
    data.players += [name]


def update_stats(players: list[str]):
    if not players:
        for name in data.players:
            data.players_db[name]['ничьих'] += 1
    else:
        winner, looser = players
        data.players_db[winner]['побед'] += 1
        data.players_db[looser]['поражений'] += 1


