"""
Вспомогательные функции.
"""

# стандартная библиотека
from configparser import ConfigParser
import configparser


# проект
import data


def read_players() -> bool:
    """Возвращает True, если в файле игроков есть хотя бы одина запись, иначе Folse. """
    config = ConfigParser()
    config.read(data.PLAYERS_PATH, encoding="utf-8")
    config = {
        player_name: {
            key: int(value)
            for key, value in config[player_name].items()
        }
        for player_name in config.sections()
    }
    data.players_db = config
    return bool(config)


def write_players() -> None:
    """
    Перезаписывает файл players.ini.
    :return:Nane
    """
    config = ConfigParser()
    for elem in data.players_db:
        config[elem] = {key: value for key, value in data.players_db[elem].items()}

    with open(data.PLAYERS_PATH, "w", encoding="utf-8") as configfile:
        config.write(configfile)
