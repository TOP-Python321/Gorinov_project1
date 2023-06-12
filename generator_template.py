def generator_template(dim: int = 3) -> str:

    """
        Генерирует и возвращает строку шаблона игрового поля. Размерность игрового поля указывается в аргументе dim
    """

    field = []
    count = 0
    width_num = len(str(dim * dim - 1))

    for _ in range(dim):
        strs = ''
        for _ in range(dim):
            strs += '{' + f"{str(count): ^{width_num}}" + '}' + ' | '
            count += 1
        field.append(strs.rstrip(' | ') + '\n')

        max_width = max([len(elem) for elem in field])
        col_sep = '—' * (max_width - 1) + '\n'
        field_out = col_sep.join(field)

    return field_out
