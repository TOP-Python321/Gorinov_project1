"""
Вспомогательные функции.
"""

# стандартная библиотека
from configparser import ConfigParser
from re import compile

# проект
import data


def read_players() -> bool:
    """Возвращает True, если в файле игроков есть хотя бы одина запись, иначе Folse. """
    config = ConfigParser()
    config.read(data.PLAYERS_PATH)
    config = {
        player_name: {
            key: int(value)
            for key, value in config[player_name].item()
        }
        for player_name in config.sections()
    }
    data.players_db = config
    return bool(config)


def write_players() -> None:
    # !!!написать!!!
    ...



