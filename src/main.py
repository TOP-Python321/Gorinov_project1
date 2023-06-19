"""
Точка входа: Управляющий код.
"""

# стандартная библиотека

# проект
import data
import help
import utils

#1. Чтение файлов данных.

# 2. ЕСЛИ первый запуск:
if utils.read_players():
    ...
    # вывод раздела помощи


# суперцикл
while True:
    # 4. Ожидание команды ввода
    command = input(data.PROMPT)

    if command in data.COMMANDS['начать новую партию']:
        ...

    elif command in data.COMMANDS['загрузить существующую партию']:
        ...

    elif command in data.COMMANDS['отобразить раздел помощи']:
        ...

    elif command in data.COMMANDS['создать или переключиться на игрока']:
        ...

    elif command in data.COMMANDS['отобразить таблицу результатов']:
        ...

    elif command in data.COMMANDS['изменить размер поля']:
        ...

    elif command in data.COMMANDS['выйти']:
        break

    # !!!отобразить раздел помощи при вводе неправильной команды!!!

# 16. обработка завершения приложения
