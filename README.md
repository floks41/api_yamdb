![Документация](hd2.jpg)


# Учебный проект YaMDb

### Разработчики:
👨🏻‍💻Роман: https://github.com/tatarenkov-r-v

👨🏼‍💻Олег: https://github.com/floks41

👨🏽‍💻Эдмон: https://github.com/MrDeadmon

:small_orange_diamond: **Пояснение.**
> Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

:yellow_circle: Когда вы запустите проект, по адресу  http://127.0.0.1:8000/redoc/ будет доступна :book: документация для API
## Как запустить проект:

### Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:tatarenkov-r-v/api_yamdb.git
```

### Cоздать и активировать виртуальное окружение на Linux / Mac:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

### Cоздать и активировать виртуальное окружение на Windows:

```
python -m venv env
```
```
\env\Scripts\activate.bat
```
### Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

### Выполнить миграции:

```
cd api_yamdb
```
```
python3 manage.py migrate
```
### Запустить проект:

```
python3 manage.py runserver

```
### Для того, чтобы заполнить базу данных контентом из приложенных csv-файлов выполните следующую команду:

```
python3 manage.py load_data

```
### Документация к API проекта:

Перечень запросов можно посмотреть в описании API

```
http://127.0.0.1:8000/redoc/
```
