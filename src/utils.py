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


def read_save() -> None:
    """
    Записывает в data.saves_db данные полученные из файла saves.txt.
    """
    saves = data.SAVES_PATH.read_text(encoding='utf-8').split('\n')
    if ''.join(saves):
        for save in saves:
            players, turns, dim = save.split('!')
            data.saves_db |= {
                tuple(players.split(',')): {
                    'dim': int(dim),
                    'turns': {
                        int(turn): data.TOKENS[i % 2]
                        for i, turn in enumerate(turns.split(','))
                    },
                }
            }


def write_saves() -> None:
    """
     Записывает незавершенные партии в файл saves.txt
    """
    texts = ''
    for key in data.saves_db:
        text = '!'.join([','.join(str(i) for i in key), ','.join(str(elem) for elem in data.saves_db[key]['turns']),
                         str(data.saves_db[key]['dim'])]) + '\n'
        texts += text

    with open(data.SAVES_PATH, "w", encoding="utf-8") as file:
        file.write(texts.rstrip('\n'))


def change_dim(new_dim: int) -> None:
    """
    Принимает int объект и перезаписывает переменные data.dim, data.dim_range, data.all_cell = new_dim**2.
    """
    data.dim = new_dim
    data.dim_range = range(new_dim)
    data.all_cells = new_dim**2
    # выигрышные комбинации
    data.winning_combinations = counts_combinations(new_dim)
    # словарь координат игрового поля c пробелами
    data.board = dict.fromkeys(range(1, data.all_cells + 1), ' ')
    # шаблон игрового поля
    data.field = field_template()


def dim_input() -> int:
    """
    Запрашивает число и проверяет ввод на соответствие шаблону, передает число как объект int.
    """
    while True:
        dim = input(f" {data.MESSAGES['ввод размерности']}{data.PROMPT}")
        if data.DIM_PATTERN.fullmatch(dim):
            return int(dim)
        print(f" {data.MESSAGES['некорректная размерность']} ")


def counts_combinations(dim: int) -> tuple[set[int]]:
    """Генерирует  и возвращает кортеж , который содержит множества выигрышных комбинаций.

    :param dim -- принимает размер игрового поля (int)
    """
    list_com = []
    list_ref = list(range(1, dim*dim + 1))

    step_row = 0
    step_col = 0

    # КОММЕНТАРИЙ: в один цикл — одобряю!
    for _ in range(dim):
        set_row = set(list_ref[step_row:dim+step_row])
        list_com.append(set_row)
        set_col = set(list_ref[step_col::dim])
        list_com.append(set_col)
        step_row += dim
        step_col += 1

    list_com.append(set(list_ref[dim-1::dim-1][:-1]))
    list_com.append(set(list_ref[::dim+1]))

    return tuple(list_com)


def output_coordinates(dim: int) -> str:
    """
    Формирует и возвращает игровое поле с координатами в виде объекта str.
    """
    # СДЕЛАТЬ: при почти полном повторении кода из предыдущей функции вам обязательно должна была прийти в голову мысль о том, что это неоптимально, и что надо бы как-то использовать уже написанную функцию (возможно, немного её доработав) — подумайте всё-таки в эту сторону
    field = []
    count = 1
    width_num = len(str(dim * dim))

    for _ in range(dim):
        strs = ''
        for _ in range(dim):
            str_lin = str(count)
            # ИСПРАВИТЬ: пробел является заполнителем по умолчанию, поэтому может быть опущен в f-строке
            strs += ' ' f"{str_lin:^{width_num}}" + ' |'
            count += 1
        field.append(strs.rstrip('|'))
        col_sep = '\n' + '—' * ((width_num + 3)*dim - 1) + '\n'
        field_out = col_sep.join(field)

    return field_out


def field_template(data_width: int = None) -> str:
    """
    Генерирует и возвращает строку шаблона игрового поля.
    :param data_width: указывается максимальная длина элемента. Без аргумента возвращает шаблон для игрового полля, при
    указании аргумента выводит шаблон для координат игрового поля.
    :return: str
    """
    if data_width is None:
        field_width = data.dim * (3 + max(len(t) for t in data.TOKENS)) - 1
    else:
        field_width = data.dim * (3 + data_width) - 1
    v_sep, h_sep = '|', '—'
    v_sep = v_sep.join([' {} '] * data.dim)
    h_sep = f'\n{h_sep * field_width}\n'
    return h_sep.join([v_sep] * data.dim)


def save_game() -> None:
    """Сохраняет текущую партию в data.saves_db"""
    data.saves_db[tuple(data.players)] = dict(zip(('dim', 'turns'), (data.dim, data.turns)))


def concatenate_rows(
        matrix1: str,
        matrix2: str,
        *matrices: str,
        padding: int = 0
) -> str:
    """
    Принимает строки. Складывает каждую строчку до символа конца строки каждой строки через определенное количество
    пробелов.
    padding: принимает количество пробелов.
    """
    matrices = matrix1, matrix2, *matrices
    matrices = [m.split('\n') for m in matrices]
    padding = ' ' * padding
    return '\n'.join(
        padding.join(row)
        for row in zip(*matrices)
    )
