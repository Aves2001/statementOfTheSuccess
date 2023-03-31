
# Statement Of The Success


## Автори

- [@Aves2001](https://www.github.com/Aves2001)
- [@SashaBenzar](https://www.github.com/SashaBenzar)
- [@IvanOstapiv](https://www.github.com/IvanOstapiv)


## Як запустити сайт

### 1. Клонуйте проект:

```bash
git clone https://github.com/Aves2001/statementOfTheSuccess.git
```

### 2. Перейдіть до каталогу проекту:

```bash
cd statementOfTheSuccess
```

### 3. Створіть віртуальний простір:

```bash
python -m venv venv
```

### 4. Актиуйте віртуальний простір:
```bash
cmd /k "cd venv\Scripts & activate"
```

### 5. Установіть залежності:

```bash
pip install -r requirements.txt
```

### 6. Перейдіть в каталог з файлом manage.py:

```bash
cd ../../statementOfTheSuccess
```

### 7. Створіть .env файл, в каталозі з файлом manage.py, з допомогою мишки, або команди:
```bash
copy con .env
```
*Примітка: щоб зберігти файл, при використанні **copy con** необхідно виконати наступні дії:*

- **CTRL + Z**
- **ENTER**

### 8. Формат файлу можна зрозуміти з прикладу:
```bash
DEBUG=on
SECRET_KEY=ваш-секретний-ключ
```

***SECRET_KEY*** - *має бути складним, від цього залежить безпека сайту.*

Згенерувати SECRET_KEY можна на сайті: https://djecrety.ir/

Приклад: ```SECRET_KEY=fe^(*%vy3#^isj(@^ao+mbcbd_21^!69hs_m!^6z&io1vtg11x```


### 9. Виконайте міграції:

```bash
manage.py makemigrations
manage.py migrate
```

### 10. Запустіть сервер:

```bash
manage.py runserver
```
 

