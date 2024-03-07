![Документация](hd2.jpg)


# API (бекенд) социальной платформы для публикации отзывов на фильмы

### Разработчики:
👨🏻‍💻Роман Татаренков: https://github.com/tatarenkov-r-v

👨🏼‍💻Олег Чужмаров: https://github.com/floks41

👨🏽‍💻Эдмон Айвазян: https://github.com/MrDeadmon

## Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)

- Python 3.9
- Django 3.2
- Django REST framework 3.12.4
- Django REST framework simple JWT 4.7.2

:small_orange_diamond: **Пояснение.**
> Проект API для социальной платформы для публикации отзывов на фильмы собирает отзывы пользователей на произведения. Сами произведения в проекте не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

:yellow_circle: Когда вы запустите проект, по адресу  http://127.0.0.1:8000/redoc/ будет доступна :book: документация для API
## Как запустить проект:

### Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:floks41/api_yamdb.git
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
