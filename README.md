REST API diary_apidocker:

Описание проекта:

REST API приложения для создания и получения дневника и его записей.

Запуск приложения:

Клонируйте репозиторий: git clone https://github.com/Cr7diesel/DiaryApi.git

Перейдите в склонированный каталог проекта

Создание переменной окружения:

Создайте файл .env и внесите данные из .env.example

Запуск приложения:

Откройте терминал => перейдите в каталог проекта =>
запустите приложение с помощью команды: docker-compose up --build

Для использования приложения нужно зарегистрироваться по адресу: /api/v1/register/

После этого необходимо авторизоваться с помощью кнопки log_in 

Создание суперпользователя:

Выполните команду: docker-compose run diary_api python3 manage.py createsuperuser

Введите все необходимые данные

Запуск тестов:

Выполните команду: docker-compose run diary_api pytest

Стэк:

Django, Django REST Framework, Docker, docker-compose, Postgresql, Celery, Redis, drf-spectacular, black, pytest, pytest-factoryboy, Faker.