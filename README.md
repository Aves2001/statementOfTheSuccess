
# Statement Of The Success


## Authors

- [@Aves2001](https://www.github.com/Aves2001)
- [@SashaBenzar](https://www.github.com/SashaBenzar)
- [@IvanOstapiv](https://www.github.com/IvanOstapiv)


## Як запустити сайт

Клонуйте проект

```bash
  git clone https://github.com/Aves2001/statementOfTheSuccess.git
```

Перейдіть до каталогу проекту

```bash
  cd statementOfTheSuccess
```

Створіть віртуальний простір

```bash
  python -m venv venv
```

Установіть залежності

```bash
  cmd /k "cd venv\Scripts & activate & cd /d ../../ & pip install -r requirements.txt"
```

Створіть .env файл, з допомогою мишки, або команди
```bash
  nul> statementOfTheSuccess/.env
```
Формат файлу можна зрозуміти з прикладу:

```bash
DEBUG=on
SECRET_KEY=ваш-секретний-ключ

```

Запустіть сервер

```bash
  cmd /k "cd venv\Scripts & activate & cd /d ../../statementOfTheSuccess & python manage.py runserver"
```
 

