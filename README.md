# Дипломный проект - DRF_AL_AUTH

## Конфигурация проекта

Необходимо создать и активировать виртуальное окружение (Linux)

```
virtualenv <env_name>
source <env_name>/bin/activate
```

Установить все зависимости проекта в requirements.txt

```
pip install -r requirements.txt
```

Провести необходимые миграции

```
python manage.py makemigrations

python manage.py migrate
```

Насладиться запуском проекта

```
python manage.py runserver
```

Создание суперпользователя для входа в админ панель

```
python manage.py createsupersuer
```

## Конфигурация базы данных

Вход в интерактивную сессию PostgreSQL

```
sudo -u postgres psql
```

Создание БД

```
CREATE DATABASE <myproject_db>;
```

Создание пользователя

```
CREATE USER <myprojectuser> WITH PASSWORD 'password';
```

Задать необходимые привилегии

```
ALTER ROLE <myprojectuser> SET client_encoding TO 'utf8';
ALTER ROLE <myprojectuser> SET default_transaction_isolation TO 'read committed';
ALTER ROLE <myprojectuser> SET timezone TO 'UTC';
```

Полномочие пользователя <myprojectuser> над бд <myproject_db>

```
GRANT ALL PRIVILEGES ON DATABASE <myproject_db> TO <myprojectuser>;
```

Выход из сессии
```
\q или \exit
```