
# Statement Of The Success


## Автори

- [@Aves2001](https://www.github.com/Aves2001)
- [@SashaBenzar](https://www.github.com/SashaBenzar)
- [@IvanOstapiv](https://www.github.com/IvanOstapiv)


## Як запустити сайт
*Примітка: в проекті використовується Python 3.8.10*

### 1. Клонуйте проект:

```cmd
git clone https://github.com/Aves2001/statementOfTheSuccess.git
```

### 2. Перейдіть до каталогу проекту:

```cmd
cd statementOfTheSuccess
```

### 3. Створіть віртуальний простір:

```cmd
python -m venv venv
```

### 4. Актиуйте віртуальний простір:
```cmd
cmd /k "cd venv\Scripts & activate & cd ../../"
```

### 5. Установіть залежності:

```cmd
pip install -r requirements.txt
```

### 6. Перейдіть в каталог з файлом manage.py:

```cmd
cd statementOfTheSuccess
```

### 7. Створіть .env файл, в каталозі з файлом manage.py, з допомогою мишки, або команди:
```cmd
copy con .env
```
*Примітка: щоб зберігти файл, при використанні **copy con** необхідно виконати наступні дії:*

- **CTRL + Z**
- **ENTER**

### 8. Формат файлу можна зрозуміти з прикладу:
```env
DEBUG=on
SECRET_KEY=ваш-секретний-ключ
```

***SECRET_KEY*** - *має бути складним, від цього залежить безпека сайту.*

Згенерувати SECRET_KEY можна на сайті: https://djecrety.ir/

Приклад: ```SECRET_KEY=fe^(*%vy3#^isj(@^ao+mbcbd_21^!69hs_m!^6z&io1vtg11x```

### 9. Виконайте міграції:

```cmd
manage.py makemigrations
manage.py migrate
```

### 10. Створіть супер-користувача:

```cmd
manage.py createsuperuser
```

### 11. Запустіть сервер:

```cmd
manage.py runserver
```
