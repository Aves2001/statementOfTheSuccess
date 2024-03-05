import os
import subprocess
import sys
import pkg_resources
from pathlib import Path

from getpass import getpass
from string import ascii_letters, digits
from random import choice
from dotenv import dotenv_values, set_key

try:
    is_Module_Not_Found = False
    import click
except ModuleNotFoundError:
    is_Module_Not_Found = True
    subprocess.run(["pip", "install", "click"])
    import click

PATH_MANAGE = "manage.py"
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = '.env'

os.chdir(BASE_DIR)
dotenv_values(ENV_FILE)


def generate_secret_key(length=50, chars=ascii_letters + digits):
    return ''.join(choice(chars) for _ in range(length))


def prompt_database():
    database = click.prompt("Яку базу даних ви будете використовувати?",
                            type=click.Choice(['psql', 'sqlite3']),
                            show_choices=True)
    menu = Menu()
    menu.add_menu_item("1", lambda: "asd")
    database = menu.loop(select=True)
    print(database)
    set_key(ENV_FILE, 'DATABASE', database)


def prompt_database_fields(database):
    if database == 'psql':
        set_key(ENV_FILE, 'DB_NAME', click.prompt("Назва бази даних", default="mydatabase"))
        set_key(ENV_FILE, 'DB_USER', click.prompt("Ім'я користувача", default="postgres"))
        set_key(ENV_FILE, 'DB_PASSWORD', getpass("Пароль"))
        set_key(ENV_FILE, 'DB_HOST', click.prompt("Хост", default='localhost'))
        set_key(ENV_FILE, 'DB_PORT', click.prompt("Порт", default='5432'))
    elif database == 'sqlite3':
        set_key(ENV_FILE, 'DB_NAME', click.prompt("Назва бази даних", default="mydatabase"))
    else:
        click.echo("Невірно вказана база даних.")


def prompt_secret_key():
    if 'SECRET_KEY' not in dotenv_values(ENV_FILE):
        set_key(ENV_FILE, 'SECRET_KEY', generate_secret_key())


def prompt_debug_mode():
    if 'DEBUG' not in dotenv_values(ENV_FILE):
        set_key(ENV_FILE, 'DEBUG', str(click.confirm("Увімкнути режим дебагу?")))


def __run_configuration_wizard():
    click.echo("Потрібно налаштувати ваше середовище.")
    prompt_database()
    prompt_database_fields(dotenv_values(ENV_FILE)['DATABASE'])
    prompt_secret_key()
    prompt_debug_mode()
    click.echo("Налаштування завершені!")


def configure():
    if 'DATABASE' not in dotenv_values(ENV_FILE) or 'DB_NAME' not in dotenv_values(ENV_FILE):
        __run_configuration_wizard()
    else:
        click.echo("Змінні середовища вже встановлені. Ось їх значення:")
        for key, value in dotenv_values(ENV_FILE).items():
            click.echo(f"{key}: {value}")


###########################################################


def install_dependencies(requirements_file=None):
    if requirements_file is None:
        requirements_file = "requirements.txt"
    click.echo("Встановлення залежностей...")
    try:
        subprocess.run(["pip", "install", "-r", requirements_file], check=True)
        click.echo("Залежності успішно встановлено.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Помилка при встановленні залежностей: {e}")


class MenuItem:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def execute(self):
        try:
            self.function()
        except Exception as e:
            click.secho(f"Помилка: {e}", fg='red')


class Menu:
    def __init__(self):
        self.menu_items = []

    def add_menu_item(self, name: str, function):
        menu_item = MenuItem(name, function)
        self.menu_items.append(menu_item)

    def display(self):
        click.echo("Пункти меню:")
        for index, menu_item in enumerate(self.menu_items, start=1):
            click.echo(f"{index}. {menu_item.name}")

    def execute_command(self, choice_input: int, select=False):
        try:
            if 1 <= int(choice_input) <= len(self.menu_items):
                menu_item = self.menu_items[choice_input - 1]

                if select:
                    return menu_item
                else:
                    menu_item.execute()
            else:
                raise ValueError
        except (ValueError, IndexError):
            raise click.BadParameter("Недопустимий номер пункту меню")

    def loop(self, select: bool):
        while True:
            try:
                self.display()
                choice_input = click.prompt("\nВиберіть пункт меню (або 'q' для виходу)")
                try:
                    if choice_input.lower() in ['q', 'exit', 'quit']:
                        break
                except click.BadParameter as e:
                    print(e)

                self.execute_command(int(choice_input), select=select)
            except click.BadParameter as e:
                click.secho(f"Недопустимий ввід: {e}", fg='red')
            except Exception as e:
                click.secho(f"Помилка: {e}", fg='red')

            click.pause("Натисніть щоб продовжити")
            click.clear()


def setup_django_project():
    click.echo("Схоже ви вперше запускаєте цей проект.")
    if click.confirm("Бажаєте виконати встановлення та налаштування Django проекта?", default=True):
        install_dependencies()

        edit_env_file()
        run_migrations()
        create_superuser()

        if click.confirm("Бажаєте запустити сервер?", default=True):
            start_server()


def start_server():
    click.echo("Запуск сервера...")
    subprocess.run([sys.executable, PATH_MANAGE, "runserver"], check=True)


def edit_env_file():
    click.echo("Редагування файлу .env...")
    configure()


def run_migrations():
    click.echo("Виконання міграцій...")
    subprocess.run([sys.executable, PATH_MANAGE, "makemigrations"])
    subprocess.run([sys.executable, PATH_MANAGE, "migrate"])


def create_superuser():
    click.echo("Створення суперкористувача...")
    subprocess.run([sys.executable, PATH_MANAGE, "createsuperuser"])


def start_shell():
    click.echo("Запуск шелу...")
    subprocess.run([sys.executable, PATH_MANAGE, "shell"])


def update_pip():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        print("Пакет pip успішно оновлено.")
    except subprocess.CalledProcessError as e:
        print(f"Помилка при оновленні пакету pip: {e}")


def check_required_packages(requirements_file=None):
    if requirements_file is None:
        requirements_file = "requirements.txt"
    package_not_found = False

    with open(requirements_file, 'r') as file:
        required_packages = []
        for i in file.read().splitlines():
            required_packages.append(str(i.split("==")[0]))

    for package in required_packages:
        try:
            dist = pkg_resources.get_distribution(package)
            print(f"Бібліотека {dist.key} версії {dist.version} встановлена.")
        except pkg_resources.DistributionNotFound:
            click.secho(f"Бібліотека {package} відсутня.", fg='red')
            package_not_found = True
    return package_not_found


def test():
    print(sys.executable)
    print(sys.prefix)


def setup_menu():
    main_menu = Menu()
    main_menu.add_menu_item("Запустити сервер", start_server)
    main_menu.add_menu_item("Встановити залежності", install_dependencies)
    main_menu.add_menu_item("Редагувати файл .env", edit_env_file)
    main_menu.add_menu_item("Виконати міграції", run_migrations)
    main_menu.add_menu_item("Створити суперкористувача", create_superuser)
    main_menu.add_menu_item("Запустити шелл", start_shell)
    main_menu.add_menu_item("Перевірити оновлення для pip", update_pip)
    main_menu.add_menu_item("test", test)
    return main_menu


def main():
    if is_Module_Not_Found or "--CREATE_VENV" in sys.argv:
        is_package_not_found = check_required_packages()
        if is_package_not_found:
            setup_django_project()

    click.clear()

    menu = setup_menu()
    menu.loop(False)


if __name__ == "__main__":
    main()
