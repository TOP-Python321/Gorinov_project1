"""
Точка входа: Управляющий код.
"""

# стандартная библиотека

# проект
import data
import help
import utils
import player
import game


# 1. Чтение файлов данных.
# 2. ЕСЛИ первый запуск:
if not utils.read_players():
    print('Игра ХО')
    # вывод титров

# 3. Запрос имени игрока
player.get_players_name()

# суперцикл
while True:
    # 4. Ожидание команды ввода
    command = input(f"{data.MESSAGES['команда']}{data.PROMPT}")

    if command in data.COMMANDS['начать новую партию']:
        # 5 запрос режима игры
        game.game_mode()

        # 8. запрос очерёдности ходов
        player.turn_order(input(f"{data.MESSAGES['очередь']} {data.players[1]}{data.PROMPT}"))

        result = game.game()
        if result is not None:
            player.update_stats(result)
        # сохранение данных в players.ini
        utils.write_players()

    elif command in data.COMMANDS['загрузить существующую партию']:
        # game.load()
        result = game.game()
        if result is not None:
            player.update_stats(result)

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
    # КОММЕНТАРИЙ: да, но желательно не весь — при вводе неправильной команды информация, например, о правилах игры не сильно поможет

# 16. обработка завершения приложения
