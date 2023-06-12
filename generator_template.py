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
            str_lin = ' {' + str(count) + '}' + ' |'
            strs += str_lin            
            count += 1
        field.append(strs.rstrip(' | ') + '\n')

        max_width = width_num * dim - 1
        col_sep = '—' * (max_width) + '\n'
        field_out = col_sep.join(field)

    return field_out
    
# Создает только поле для Х или 0. Без ввода координат.
