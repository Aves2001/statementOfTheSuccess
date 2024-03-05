import msvcrt
import sys

from MenuItem import MenuItem
from availability_check import *
from function import *

is_colorama = False
try:
    from colorama import init, Fore, Style

    is_colorama = True
except ImportError:
    print("Бібліотека 'colorama' не встановлена.")
    print("Встановіть залежності для нормального відображення меню.")


def check_python_version():
    if sys.version_info < (3, 8):
        print("Потрібна версія Python 3.8 або вище.")
        print("Скачайте та встановіть його: https://www.python.org/downloads/release/python-3810/")
        input()
        sys.exit(1)


class Menu:
    def __init__(self, menu_Items, colorama=True):
        self.menu_items = menu_Items
        self.is_colorama = colorama

        self.color_green = ""
        self.color_red = ""
        self.RESET = ""
        self.RESET_ALL = ""

        self.check_is_colorama()

        self.env_values = {
            "DB_HOST": "",
            "DB_NAME": "",
            "DB_USER": "",
            "DB_PASSWORD": "",
        }

    def check_is_colorama(self):
        if self.is_colorama:
            init()
            self.color_green = Fore.LIGHTGREEN_EX
            self.color_red = Fore.LIGHTRED_EX
            self.RESET_ALL = Style.RESET_ALL
            self.RESET = Fore.RESET

    def run_server(self):
        print("Запуск сервера")
        subprocess.run([VENV_PYTHON, PATH_MANAGE, "runserver"])

    def create_virtual_environment(self):
        print("Створення віртуального середовища...")
        subprocess.run(["python", "-m", "venv", "venv"])

    def install_requirements(self):
        print("Встановлення залежностей...")
        subprocess.run([VENV_PIP, "install", "-r", "requirements.txt"])

    def load_env_values(self):
        try:
            with open(PATH_ENV_FILE, "r") as env_file:
                for line in env_file:
                    key, value = line.strip().split("=")
                    if key in self.env_values:
                        self.env_values[key] = value
        except FileNotFoundError:
            pass

    def edit_env_file(self):
        print("Редагування файлу .env...")
        self.load_env_values()

        for key in self.env_values:
            value = self.env_values[key]
            new_value = input(f"Введіть значення для {key} [{value}]: ")
            self.env_values[key] = new_value if new_value else value

        with open(PATH_ENV_FILE, "w") as env_file:
            for key, value in self.env_values.items():
                env_file.write(f"{key}={value}\n")

    def run_migrations(self):
        print("Виконання міграцій...")
        subprocess.run(["venv/Scripts/python", "statementOfTheSuccess/manage.py", "makemigrations"])
        subprocess.run(["venv/Scripts/python", "statementOfTheSuccess/manage.py", "migrate"])

    def create_superuser(self):
        print("Створення суперкористувача...")
        subprocess.run(["venv/Scripts/python", "statementOfTheSuccess/manage.py", "createsuperuser"])

    def print_menu(self):
        print("\n")
        for menu_item in self.menu_items:
            menu_item: MenuItem
            availability = menu_item.get_availability()

            if availability:
                color = self.color_green
            else:
                color = self.color_red

            print(f"{color}{menu_item}{self.RESET_ALL}")

        print(f"\n{self.color_green}[0] Вийти{self.RESET_ALL}")

    def start(self):
        # get_choice = msvcrt.getch if sys.platform.startswith('win') else input
        get_choice = input
        self.print_menu()
        while True:
            try:
                choice = int(get_choice())
            except:
                continue

            if choice == 0:
                exit()

            if 0 <= choice <= len(self.menu_items):
                for item in self.menu_items:
                    item: MenuItem
                    if item.number == choice and item.get_availability():
                        item.function()
                    else:
                        print(item.error_message)
            else:
                print("Недійсний вибір. Будь ласка, спробуйте ще раз.\n")


if __name__ == "__main__":
    menu_items = (
        MenuItem("Запустити сервер", Menu.run_server, [is_env_file, ]),
        MenuItem("Створити віртуальне середовище", Menu.create_virtual_environment),
        MenuItem("Встановити залежності", Menu.install_requirements),
        MenuItem("Редагувати файл .env", Menu.edit_env_file, is_env_file),
        MenuItem("Виконати міграції", Menu.run_migrations),
        MenuItem("Створити суперкористувача", Menu.create_superuser),
    )

    menu = Menu(menu_Items=menu_items, colorama=is_colorama)
    menu.start()
