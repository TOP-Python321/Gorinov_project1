def generator_template(dim: int = 3) -> str:
    """
    Генерирует и возвращает строку шаблона игрового поля. Размерность игрового поля указывается в аргументе dim.
    """
    field = []
    width_num = 4

    # КОММЕНТАРИЙ: генераторные выражения во вложенных join() удобнее хотя бы тем, что после их работы не нужно обрезать лишние символы — в то время, как у вас выполняется довольно много действий, без которых можно было бы обойтись
    for _ in range(dim):
        strs = ''
        for _ in range(dim):
            # ИСПРАВИТЬ: почему бы не записать это в один литерал — в чём магия?
            strs += ' {}' + ' |'
        # ИСПРАВИТЬ: не слишком хорошо, что в строчке с ходами у вас на один пробел меньше
        field.append(strs.rstrip(' | ') + '\n')
        col_sep = '—' * (width_num*dim - 1) + '\n'
        field_out = col_sep.join(field)

    # ИСПРАВИТЬ: в конце итоговой строки лишний \n
    return field_out


def output_coordinates(dim: int = 3) -> str:
    """
    Формирует и возвращает игровое поле с координатами в виде объекта str.
    """
    field = []
    count = 1
    width_num = len(str(dim * dim))

    for _ in range(dim):
        strs = ''
        for _ in range(dim):
            str_lin = str(count)
            strs += ' ' f"{str_lin: ^{width_num}}" + ' |'
            count += 1
        field.append(strs.rstrip(' | ') + '\n')
        col_sep = '—' * ((width_num + 3)*dim - 1) + '\n'
        field_out = col_sep.join(field)

    return field_out


def counts_combinations(dim: int = 3) -> tuple[set[int]]:
    """Генерирует  и возвращает кортеж , который содержит множества выигрышных комбинаций.

    :param dim -- принимает размер игрового поля (int)
    """
    list_com = []
    list_ref = list(range(1, dim*dim + 1))

    step_row = 0
    step_col = 0

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

