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


def generator_template(dim: int) -> str:
    """
    Генерирует и возвращает строку шаблона игрового поля. Размерность игрового поля указывается в аргументе dim.
    """
    field = []
    width_num = 4

    # КОММЕНТАРИЙ: генераторные выражения во вложенных join() удобнее хотя бы тем, что после их работы не нужно обрезать лишние символы — в то время, как у вас выполняется довольно много действий, без которых можно было бы обойтись
    # постараюсь доработать в ходе проекта
    for _ in range(dim):
        strs = ''
        for _ in range(dim):
            # ИСПРАВИТЬ: почему бы не записать это в один литерал — в чём магия?
            # между литералами еще что -то записывал и не исправил строку
            strs += ' {} |'
        # ИСПРАВИТЬ: не слишком хорошо, что в строчке с ходами у вас на один пробел меньше
        field.append(strs.rstrip('|'))
        col_sep = '\n' + '—' * (width_num*dim - 1) + '\n'
        field_out = col_sep.join(field)

    # ИСПРАВИТЬ: в конце итоговой строки лишний \n
    return field_out


def save_game() -> None:
    """Сохраняет текущую партию в data.saves_db"""
    data.saves_db[tuple(data.players)] = dict(zip(('dim', 'turns'), (data.dim, data.turns)))

