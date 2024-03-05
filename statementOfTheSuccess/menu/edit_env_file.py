from pathlib import Path

import click
from getpass import getpass
from string import ascii_letters, digits
from random import choice
from dotenv import dotenv_values, set_key

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = Path.joinpath(BASE_DIR, '.env')

dotenv_values(ENV_FILE)


def generate_secret_key(length=50, chars=ascii_letters + digits):
    return ''.join(choice(chars) for _ in range(length))


@click.group()
def cli():
    pass


def prompt_database():
    database = click.prompt("Яку базу даних ви будете використовувати? (psql/sqlite3)",
                            type=click.Choice(['psql', 'sqlite3']))
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
    click.echo("Вітаю! Потрібно налаштувати ваше середовище.")
    prompt_database()
    prompt_database_fields(dotenv_values(ENV_FILE)['DATABASE'])
    prompt_secret_key()
    prompt_debug_mode()
    click.echo("Налаштування завершені!")


@cli.command()
def configure():
    if 'DATABASE' not in dotenv_values(ENV_FILE) or 'DB_NAME' not in dotenv_values(ENV_FILE):
        __run_configuration_wizard()
    else:
        click.echo("Змінні середовища вже встановлені. Ось їх значення:")
        for key, value in dotenv_values(ENV_FILE).items():
            click.echo(f"{key}: {value}")


if __name__ == '__main__':
    cli()
