# Выполненное Тестовое задание для стажировки в юнит Market Intelligence
## О проекте
REST API сервис для проведения голосований.  
Есть возможность создать голосование с вариантами ответов, проголосовать за конкретный вариант и 
получить общие результаты голосования.  
Также реализована работа с учетными записями пользователей.  
Работа с методами сервиса голосования реализована через аутентификацию по токену.
## Технологии в проекте
Сервис реализован на языке Python 3.8 с помощью фреймворка Django 3.2 и django rest framework 3.12. В качестве базы данных используется Postgres.
Документация к методам api генерируется автоматически при помощи библиотеки drf_yasg и основана на swagger.io.  
Реализован функционал работы с учетными записями пользователей через api с помощью библиотеки djoser.  
Работа с методами сервиса голосования реализована через аутентификацию по токену.
## Запуск
1. Запуск локально у себя вручную  
   * Сделать клонирование этого репозитория ```git clone <адрес репозитория>```
   * Зайти в папку проекта под названием avito-mi-trainee-task
   * Развернуть виртуальное окружение ```python -m venv venv``` второй venv - название виртуального окружения. Можно выбрать свое
   * Активировать виртуальное окружение ```source venv/Scripts/activate```
   * Установить зависимости проекта ```pip install -r requirements.txt```
   * Установить базу данных PostgreSQL
   * Создать пользователя базы данных
   * Создать таблицу в базе данных
   * Заполнить данными поле ```DATABASES``` в файле settings.py для подключения к базе данных.  
   Записать в поля ```NAME - имя бд, USER - пользователь бд, PASSWORD - пароль пользователя бд, PORT - порт бд```
   * Создать миграции базы данных ```python manage.py makemigrations```
   * Произвести миграции ```python manage.py migrate```
   * Если будут входить в админку Django, то нужно создать суперпользователя ```python manage.py createsuperuser```  
   * Тестирование ```python manage.py test api/tests/```
   Админка тут http://127.0.0.1:8000/admin/
   * Запуск проекта ```python manage.py runserver```
2. Запуск через докер  
   * Сделать клонирование этого репозитория ```git clone <адрес репозитория>```
   * Зайти в папку проекта под названием avito-mi-trainee-task
   * Запустить контейнер ```docker-compose up -d```
   * Создать миграции базы данных ```docker-compose run web python manage.py makemigrations```
   * Произвести миграции ```docker-compose run web python manage.py migrate```
   * Зайти на адрес  http://127.0.0.1:8000/swagger/
   * Если будут входить в админку Django, то нужно создать суперпользователя ```docker-compose run web python manage.py createsuperuser```
   * Тестирование через docker ```docker-compose run web python manage.py test api/tests/```
   Админка тут http://127.0.0.1:8000/admin/ 
## Схема архитектуры  
![Схема REST API](http://dl3.joxi.net/drive/2021/06/22/0037/2710/2452118/18/59fb5621b2.jpg)  
![Схема БД](http://dl4.joxi.net/drive/2021/06/24/0037/2710/2452118/18/6e6f077c38.jpg)

## Работа с API
Сервис реализует API работающее по протоколу HTTP.  

Реализованы методы:
   * POST /api/createPoll/ создать голосование c вариантами ответов
   * POST /api/poll/ проголосовать за конкретный вариант.
   * POST /api/getResult/ получить результат по конкретному голосованию.  

Для простоты проверки советую делать все запросы через swagger http://127.0.0.1:8000/swagger/  

После разворачивания сервиса, чтобы начать работу с ним, необходимо:  
1. Создать учетную запись по адресу http://127.0.0.1:8000/auth/users/  
2. Получить токен авторизации по адресу http://127.0.0.1:8000/api/api-token-auth/
3. Указать токен в Headers Authorization запроса: Token <сгенерированное значение>  
В swagger это можно сделать нажав сюда http://joxi.ru/4AkJXkxUkOJWg2 и вставив туда значение - Token <сгенерированное значение>. Пример - http://joxi.ru/zANN7OlTjY7EBA  
Нажать кнопку Authorize.
Это необходимо проделывать каждому пользователю.
4. После этого можно создать новое голосование по адресу http://127.0.0.1:8000/api/v1/createPoll/
5. Проголосовать можно по адресу http://127.0.0.1:8000/api/v1/poll/
6. Получить результаты голосования можно по адресу http://127.0.0.1:8000/api/v1/getResult/
## Структура
```
├── api  # Приложение api для голосования.
│   ├── tests
|	 |	  ├── test_views.py  # Тесты для views.
|	 ├── admin.py  # Регистрация моделей в админке Django.
|	 ├── models.py  # Модели объектов для БД.
|	 ├── serializers.py  # Сериализаторы.
|	 ├── urls.py  # URL пути приложения.
|	 ├── views.py  # Представления, обрабатывающие запросы.
├── service_api
|   ├── settings.py  # Основные настройки проекта.
|   ├── urls.py  # Головные URL пути проекта.
└── manage.py
```
## Документация
Документация к api генерируется автоматически и доступна по адресам: http://127.0.0.1:8000/swagger/ и http://127.0.0.1:8000/redoc/
В swagger доступна возможность отправки http запросов к сервису.
## Декомпозиция задачи для создания API сервиса голосования
1. Подготовительные работы
    * Создание проекта на github
    * Клонирование проекта себе на пк
    * Создание отдельной ветки для разработки
    * Настройка виртуального окружения проекта
    * Создание проекта service_api
    * Создание приложения api
    * Выполнение миграций для создания базовых моделей Django
    * Создание суперпользователя
    * Запуск сервера для проверки работоспособности проекта
    * Настройка .gitignore
2. Создание моделей
    * Продумывание архитектуры сущностей базы данных в виде схемы
    * В Django модель User уже реализована ее и используем
    * Создание модели Poll - голосование
    * Создание модели Сhoice - вариант голосования
    * Создание модели Vote - голос пользователя
    * Регистрация моделей в админке Django
    * Выполнение миграций для создания объектов в базе данных
3. Создание сериализаторов
    * Создание 2-х сериализаторов для организации голосования. Дополнительный сериализатор нужен для модели Choice
    * Создание сериализатора для голосования пользователей
    * Создание 2-х сериализаторов для получения результата голосования. Дополнительный сериализатор нужен для модели Choice
4. Создание views
    * Создание view для организации голосования
    * Создание view для голосования пользователей
    * Создание view для получения результата голосования
5. Создание endpoints
    * Создание urls для views приложения
    * Создание urls для проекта
6. Аутентификации по токену
    * Подключение аутентификации
    * Настройка urls
7. Подключение возможности работы с учетными записями для пользователей c помощью djoser. Регистрация, изменение, восстановление пароля, удаление и т.д.
    * Подключение djoser
    * Настройка urls
8. Тестирование
    * Мануальное тестирование запросов
    * Проверка прав доступа для Авторизованного и Анонимного пользователей
    * Написание автоматических тестов для views
    * Запуск тестов
    * Проверка кода на соответсвие PEP8
12. Создание документации
    * Подключение drf_yasg
    * Настройка urls
    * Написание docstrings (изначально делается в момент написания кода)
    * Написание комментариев в сложных местах кода (изначально делается в момент написания кода)
    * Написание type hints (изначально делается в момент написания кода)
    * Создание requirements.txt - сохранение всех библиотечных зависимостей проекта
    * Написать README.md
13. Релиз
    * Установить Debug = False
    * Спрятать все ключи и пароли в переменные окружения (изначально не должны попадать в репозиторий в открытом виде)
    * Настроить запуск приложения через docker-compose up
    * Открыть репозиторий
## Усложнения
1. Написаны тесты.  
  * coverage = 97% http://joxi.ru/DmBaKMkF4eKXlr  
Проверку покрытия можно сделать ```coverage run --source='api' manage.py test api/tests``` и затем ```coverage report```.  
Если хочется в более красивом виде получить отчет, то можно использовать ```coverage html```. В папке с проектом появится папка htmlcov в ней нужно запустить index.html
2. Опишите, как изменится архитектура, если мы ожидаем большую нагрузку  
  * На вход системы можно поставить балансировщик нагрузки (например nginx). Он будет перенаправлять запросы на несколько экземпляров нашего приложения.
3. Опишите, как можно защититься от накруток.  
  * Для борьбы с накрутками я реализовал регистрацию пользователей. Только зарегистрированные пользователи получившие токен авторизации могут проголосовать. Также каждая учетная запись может проголосовать в каждом голосовании только один раз. Если пойти дальше, можно потребовать обязательную регистрацию с email.
4. Попробуйте оценить, какую нагрузку в RPS сможет выдержать ваш сервис  
  * Нагрузку оценивал с помощью ApacheBench (ab). Для 1000 запросов с разными Concurrency Level. Измерения делались для метода POST /api/v1/getResult/  
Пример команды: ab -T "application/json" -c 1 -n 1000 -p post.json http://127.0.0.1:8000/api/v1/getResult/  
В среднем метод POST /api/v1/getResult/ обрабатывает 20 запросов в секунду.
Результаты:  

| concurrency       | requests                | rps |
| :-------------: |:------------------:| :-----:|
|  1  | 1000  | 12,61 |
|  51	| 1000  | 21,53 |
| 101 | 1000 | 21,71 |
| 151 | 1000 | 20,91 |
| 201 | 1000 | 21,62 |
| 251 | 1000 | 20,88 |
| 501 | 1000 | 21,72 |
| 951 | 1000 | 20,86 |
|     | Сред.| 20,23 |
| 101 | 10000 | 18,96 |






