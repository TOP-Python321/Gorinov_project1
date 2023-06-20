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
