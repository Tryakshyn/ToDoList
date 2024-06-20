import os
import sys


def main():
    # Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE на 'todo_app.settings'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_app.settings')
    try:
        # Пытаемся импортировать функцию execute_from_command_line из django.core.management
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Если возникает ошибка ImportError, выводим сообщение об ошибке
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Вызываем функцию execute_from_command_line с аргументами командной строки sys.argv
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Если скрипт запускается напрямую (а не импортируется как модуль), вызываем функцию main()
    main()
