import os



def is_env_file():
    return (
        os.path.isfile("statementOfTheSuccess/.env"),
        "Файл env не знайдено"
    )


def check_required_env_values(required_fields):
    load_env_values()
    for field in required_fields:
        if not env_values[field]:
            return False
    return True