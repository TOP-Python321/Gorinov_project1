def generator_template(dim: int = 3) -> str:

    """
        Генерирует и возвращает строку шаблона игрового поля. Размерность игрового поля указывается в аргументе dim
    """

    field = []
    count = 0
    width_num = 4

    for _ in range(dim):
        strs = ''

        for _ in range(dim):
            strs += ' {' + str(count) + '}' + ' |'
            count += 1
        field.append(strs.rstrip(' | ') + '\n')
        col_sep = '—' * (width_num * dim - 1) + '\n'
        field_out = col_sep.join(field)

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
        col_sep = '—' * ((width_num + 3) * dim - 1) + '\n'
        field_out = col_sep.join(field)

    return field_out