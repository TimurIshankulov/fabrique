# Сервис рассылок Fabrique.studio

## Инструкция по установке и запуску

0) Установить пакеты:
```
sudo apt-get install -y libpq-dev python3.10-venv python3-dev build-essential
```
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
cp fabrique/config_template.py fabrique/config.py
```
5) Указать параметры подключения к СУБД PostgreSQL в файле config.py: имя БД, пользователь, пароль, хост и порт. Также необходимо указать Bearer-токен для аутентификации в сервисе отправки сообщений.
6) В settings.py указать параметры подключения к СУБД Redis: REDIS_HOST и REDIS_PORT.
7) Провести миграцию:
```
python manage.py migrate
```
9) Запустить сервер Django:
```
python manage.py runserver
```
8) Запустить Celery в отдельном окне терминала, не забыв активировать виртуальное окружение:
```
cd <папка/с/проектом>
source .venv/bin/activate
celery -A fabrique worker -l info
```
9) Запустить Celery Beat в отдельном окне терминала:
```
cd <папка/с/проектом>
source .venv/bin/activate
celery -A fabrique beat -l info
```
## Документация по API

https://documenter.getpostman.com/view/9290909/VUjPHk2G
