### API для проекта YaMDB в рамках Яндекс.Практикум

Поддерживаемые методы запросов:

```
GET, POST, PUT, PATCH, DELETE
```
Формат выходных данных:

```
JSON
```


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:AnnPovor/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Установить в папку api_yamdb:

```
cd api_yamdb
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
Подробная документация по работе API:
```
По адресу http://127.0.0.1:8000/redoc/ доступна документация для API YaMDB
```