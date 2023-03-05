![Workflow](https://github.com/drink-and-talk/drink_n_talk_backend/actions/workflows/drink_n_talk_deploy.yml/badge.svg)

![Python](https://img.shields.io/badge/Python-3.10.9-blue?style=flat&logo=python&logoColor=yellow)
![Django](https://img.shields.io/badge/Django-4.0-red?style=flat&logo=django&logoColor=blue)


# Drink&Talk ™
## Бэкенд для PET-проекта

Идеей проекта является веб-сервис, позволяющий пользователям искать единомышленников и общаться посредством групповой on-line видео-конференции.
Критерии для подбора единомышленников:
+ язык общения
+ интересующая тема
+ характер пользователя (любите слушать или говорить)

Отличительной особенностью сервиса явлется возможность присоединиться к разговору пользователей, которые решили пропустить по стаканчику и поговорить на интересующую тему. Для этого достаточно выбрать напиток, который в данный момент плещется у Вас в стакане, или указать в настройках профиля уровень Ваших алкогольных предпочтений.

## Порядок установки проекта

Клонируем репозиторий и переходим в директорию с приложением:
```
git clone https://github.com/drink-and-talk/drink_n_talk_backend.git
```
```
cd ./drink_n_talk_backend/infra/
```

### Структура env-файла:

#### _Первый способ (если необходимо изменить имя БД или ещё что то)_:
Создаем и открываем для редактирования файл `.env`:
```
sudo nano .env
```
В файл вносим следующие данные:
```
# секретный ключ для Django
SECRET_KEY="django-insecure-__athl8^e51(0)zch#jgb3curg0k8wf!ivae9#z)q6e18^km@s"
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

#### _Второй способ (если Вас всё устраивает и так)_:
Просто изменяем название файла `envexample`, находящегося в репозитории данного проекта, на `.env`.

### Развертывание с использованием Docker:

Разворачиваем контейнеры в фоновом режиме:
```
sudo docker-compose up -d
```
При первом запуске выполняем миграции:
```
sudo docker-compose exec backend python manage.py migrate
```
При первом запуске собираем статику:
```
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
Загружаем данные в базу:
```
sudo docker-compose exec backend python manage.py loaddata languages.json
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