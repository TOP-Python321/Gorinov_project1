"""
Вспомогательные функции.
"""

# стандартная библиотека
from configparser import ConfigParser
from pathlib import Path

# проект
import data


def read_players() -> dict[str, dict[str, int]] | bool:
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

