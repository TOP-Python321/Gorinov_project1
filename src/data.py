"""
Глобальные переменные и константы.
"""

# стандартная библиотека
from pathlib import Path
from re import compile

# проект
import utils

PLAYERS_PATH = Path(r'..\data\players.ini')
SAVES_PATH = Path(r'..\data\saves.txt')


PROMPT = ' > '
MESSAGES = {
    'ввод имени': 'введите имя игрока',
    'некорректное имя': 'имя игрока должно начинаться с буквы, содержать только буквы, цифры и сивол подчеркивания',
    'режим игры': 'ведите пустую строку для игры с ботом, для игры со вторым игроком введите любой символ',
    'команда': 'введите команду',
    'ход': 'введите номер ячейки игрового поля',
    'очередь': 'введите любой символ если первым будет ходить'
}


COMMANDS = {
    'начать новую партию': ('new', 'n', 'начать', 'н'),
    'загрузить существующую партию': ('load', 'l', 'загрузка', 'з'),
    'отобразить раздел помощи': ('help', 'h', 'помощь', 'п'),
    'создать или переключиться на игрока': ('player', 'p', 'игрок', 'и'),
    'отобразить таблицу результатов': ('table', 't', 'таблица', 'т'),
    'изменить размер поля': ('dim', 'd', 'размер', 'р'),
    'выйти': ('quit', 'q', 'выход', 'в')
}


NAME_PATTERN = compile(r'[A-Za-zА-ЯЁа-яё][A-Za-zА-ЯЁа-яё\d_]+')

players_db: dict[str, dict[str, int]] = {}
saves_db: dict[tuple[str, str], dict] = {}

dim: int = 3
dim_range = range(dim)
all_cells: int = dim**2

TOKENS = ('X', '0')
players: list[str] = []

turns: dict[int] = {}

# выигрышные комбинации
winning_combinations = utils.counts_combinations(dim)

# словарь координат игрового поля c пробелами
field_coordinates = dict.fromkeys(range(1, all_cells + 1), ' ')

# шаблон игрового поля
field_template = utils.generator_template(dim)
