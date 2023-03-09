![Workflow](https://github.com/drink-and-talk/drink_n_talk_backend/actions/workflows/drink_n_talk_deploy.yml/badge.svg)

![Python](https://img.shields.io/badge/Python-3.10.9-blue?style=flat&logo=python&logoColor=yellow)
![Django](https://img.shields.io/badge/Django-4.0-red?style=flat&logo=django&logoColor=blue)


# Drink&Talk ™
## Бэкенд для PET-проекта

Идеей проекта является веб-сервис, позволяющий пользователям искать единомышленников и общаться посредством групповой видео-связи.
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
При первом запуске выполняем следующие команды:
+ применяем миграции:
```
sudo docker-compose exec backend python manage.py migrate
```
+ собираем статику:
```
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
+ загружаем тестовые данные в базу, включающие в себя: большое количество языков, небольшое количество тем для разговоров, напитков и одного тестового пользователя-администратора:
```
sudo docker-compose exec backend python manage.py loaddata data.json
```
#### Логин и пароль от учетной записи тестового пользователя-администратора:
+ _логин_
```
drink
```
+ _пароль_
```
talk2023
```

## Эндпоинты приложения

### Работа с пользователями
##### Для доступа к эндпоинтам требуется авторизация

_Получение списка пользователей: доступный метод - GET_
```
/api/v1/users/
```
_Создание нового пользователя: доступный метод - POST_
```
/api/v1/users/
```
_Схема запроса:_
```
{
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "email": "user@example.com",
    "password": "string",
    "about": "string",
    "photo": "uri",
    "birth_day": "2019-08-24",
    "degree": 0,
    "character": -1,
    "theme": [
        "string"
    ],
    "language": [
        "string"
    ]
}
```
+ _характер (character): ***-1*** - любите слушать, ***1*** - говорить_
+ _предпочтительный градус напитков (degree): ***0*** - безаклогольные, ***1*** - слабоаклогольные, ***2*** - крепкие_
+ _любимые темы для разговоров (theme): поле ***tag*** темы_
+ _язык общения (language): поле ***abbreviation*** языка_

_Получение информации о пользователе по id: доступный метод - GET_
```
/api/v1/users/{id}/
```
_Получение информации о текущем пользователе: доступный метод - GET_
```
/api/v1/users/me/
```
_Полное или частичное обновление информации о пользователе: доступные методы - PUT, PATCH_
```
/api/v1/users/me/
```
_Схема запроса:_
```
{
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "email": "user@example.com",
    "password": "string",
    "about": "string",
    "photo": "uri",
    "birth_day": "2019-08-24",
    "degree": 0,
    "character": -1,
    "theme": [
        "string"
    ],
    "language": [
        "string"
    ]
}
```
+ _характер (character): ***-1*** - любите слушать, ***1*** - говорить_
+ _предпочтительный градус напитков (degree): ***0*** - безаклогольные, ***1*** - слабоаклогольные, ***2*** - крепкие_
+ _любимые темы для разговоров (theme): поле ***tag*** темы_
+ _язык общения (language): поле ***abbreviation*** языка_

_Удаление текущего пользователе: доступный метод - DEL_
```
/api/v1/users/me/
```
_Смена пароля: доступный метод - POST_
```
/api/v1/users/set_password/
```
_Схема запроса:_
```
{
    "new_password": "string",
    "current_password": "string"
}
```
_Смена логина (username): доступный метод - POST_
```
/api/v1/users/set_username/
```
_Схема запроса:_
```
{
    "current_password": "string",
    "new_username": "string"
}
```
_Создание токена для пользователя: доступный метод - POST_
```
/api/v1/token/login/
```
_Схема запроса:_
```
{
    "password": "string",
    "username": "string"
}
```
_Удаление токена: доступный метод - DEL_
```
/api/v1/token/logout/
```
### Работа с темами

_Получение списка тем: доступный метод - GET_
```
/api/v1/themes/
```
_Получение информации о теме по id: доступный метод - GET_
```
/api/v1/themes/{id}/
```
### Работа с языками

_Получение списка языков: доступный метод - GET_
```
/api/v1/languages/
```
_Получение информации о языке по id: доступный метод - GET_
```
/api/v1/languages/{id}/
```
### Работа с напитками

_Получение списка напитков: доступный метод - GET_
```
/api/v1/drinks/
```
_Получение информации о напитке по id: доступный метод - GET_
```
/api/v1/drinks/{id}/
```
_Связывание пользователя и напитка по id: доступный метод - GET_
```
/api/v1/drinks/{id}/pour/
```
_Удалить связь пользователя и напитка по id: доступный метод - DEL_
```
/api/v1/drinks/{id}/pour/
```
### Работа с барными стойками
##### Для доступа к эндпоинтам требуется авторизация

_Получение списка существующих барных стоек (для каждого пользователя отображается список стоек, подходящий под его параметры): доступный метод - GET_
```
/api/v1/bars/
```
_Создание новой барной стойки: доступный метод - POST_
```
/api/v1/bars/
```
_Схема запроса:_
```
{
    "theme": "string",
    "language": "string",
    "degree": 0,
    "topic": "string",
    "quantity": 2
}
```
+ _тема для разговора (theme) за баром: поле ***tag*** темы_
+ _язык общения (language) за баром: поле ***abbreviation*** языка_
+ _градус напитков (degree) на баре: ***0*** - безаклогольные, ***1*** - слабоаклогольные, ***2*** - крепкие (по умолчанию устанавливается значение установленной в настройках у пользователя-инициатора или от градуса напитка, который он указал что пьет в данный момент)_
+ _коротко о чём хотелось бы поговорить (topic)_
+ _максимальное количество участников (quantity) за баром - от ***2*** до ***9***: по умолчанию - два участника_

_Получение информации о барной стойке по id: доступный метод - GET_
```
/api/v1/bars/{id}/
```
_Удалить барную стойку по id: доступный метод - DEL_
_(Удалить бар может только инициатор или администратор)_
```
/api/v1/bars/{id}/
```
_Связывание пользователя и бара по id: доступный метод - GET_
```
/api/v1/bars/{id}/to_join/
```
_Удалить связь пользователя и бара по id: доступный метод - DEL_
```
/api/v1/bars/{id}/to_join/
```
