"""
Раздел помощи.
"""
import data


def read_help() -> list:
    """Читает строки из файла help.txt и возвращает список строк"""
    with open(data.HELP_PATH, "r", encoding="utf-8") as file:
        result = file.readlines()
        return result


def read_command(list_str: list[str]) -> list:
    """Находит в списке  строки с указанным символом и возвращает список найденных строк """
    result = [line for line in list_str if '>' in line]
    return result
# !!!реализовать вывод помощи при вводе неправильной команды в main.py!!!
# СДЕЛАТЬ: реализовать возможность выводить раздел помощи как целиком, так и по частям
