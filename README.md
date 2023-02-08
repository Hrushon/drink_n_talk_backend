![Workflow](https://github.com/drink-and-talk/drink_n_talk_backend/actions/workflows/drink_n_talk_workflow.yml/badge.svg)

![Python](https://img.shields.io/badge/Python-3.10.9-blue?style=for-the-badge&logo=python&logoColor=yellow)
![Django](https://img.shields.io/badge/Django-4.0-red?style=for-the-badge&logo=django&logoColor=blue)


# Drink&Talk
## Бэкенд для проекта 

Здесь какое-то описание......

## Порядок установки проекта

Клонируем репозиторий и переходим в директорию с приложением:
```
git clone https://github.com/...
```
```
cd ./drink_n_talk_backend/infra/
```

### Структура env-файла:

Создаем и открываем для редактирования файл .env:
```
sudo nano .env
```
В файл вносим следующие данные:
```
# секретный ключ для Django
SECRET_KEY=jhvsklhglsgvnnuefc
# указываем, что работаем с postgresql
DB_ENGINE=django.db.backends.postgresql
# указываем имя базы данных
DB_NAME=postgres
# логин для подключения к базе данных
POSTGRES_USER=postgres
# пароль для подключения к БД
POSTGRES_PASSWORD=postgres
# название сервиса (контейнера) для БД
DB_HOST=db
# указываем порт для подключения к БД
DB_PORT=5432
```

### Развертывание с использованием Docker:

Разворачиваем контейнеры в фоновом режиме:
```
sudo docker-compose up -d
```
При первом запуске выполняем миграции:
```
sudo docker-compose exec web python manage.py migrate
```
При первом запуске собираем статику:
```
sudo docker-compose exec web python manage.py collectstatic --no-input
```
Загружаем данные в базу:
```
sudo docker-compose exec web python manage.py loaddata dump.json
```

## Эндпоинты приложения

### ........
```
/......../     метод: ................
```
```
/......../     методы: ................
```
```
/......../     методы: ................
```