# Учебный проект YaMDb

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:tatarenkov-r-v/api_yamdb.git
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение на Linux / Mac:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Cоздать и активировать виртуальное окружение на Windows:

```
python -m venv env
```
```
\env\Scripts\activate.bat
```
Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver

```

### Документация к API проекта:

Перечень запросов можно посмотреть в описании API

```
http://127.0.0.1:8000/redoc/
```