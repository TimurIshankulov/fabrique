# Сервис рассылок Fabrique.studio

## Инструкция по установке и запуску

1) Клонировать репозиторий:
```
git clone https://gitlab.com/tim290592/fabrique.git
cd fabrique
```
2) Создать виртуальную среду, активировать:
```
python -m venv .venv
source .venv/bin/activate
```
3) Установить зависимости:
```
python -m pip install -r requirements.txt
```
4) Скопировать файл config_template.py, переименовав его в config.py:
```
cp config_template.py config.py
```
5) Указать параметры подключения к СУБД PostgreSQL в файле config.py: имя БД, пользователь, пароль, хост и порт. Также необходимо указать Bearer-токен для аутентификации в сервисе отправки сообщений.
6) В settings.py указать параметры подключения к СУБД Redis: REDIS_HOST и REDIS_PORT.
7) Запустить сервер Django:
```
python /.manage.py runserver
```
8) Запустить Celery:
```
celery -A fabrique worker -l info
```
9) Запустить Celery Beat:
```
celery -A fabrique beat -l info
```
## Документация по API

https://documenter.getpostman.com/view/9290909/VUjPHk2G
