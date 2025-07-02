# API для бронирования отеля
##### Пробую разные технологии и паттерны в рамках курса по Backend-разработки на FastApi.
***
# Полезные команды
***
## Связывание локального Git'а и GitHub
``````
git remote add main https://github.com/DrHy6yC/course_booking_hotel.git
``````
***
## Активация виртуального окружения
``````
python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
``````
***
## Работа с внешними библиотеками
### 1. Установка библиотек из requirements.txt
``````
pip install -r requirements.txt
``````
### 2. Добавление установленных библиотек в requirements.txt
``````
pip freeze >requirements.txt
``````
***
##  Запуск проекта
``````
python src/main.py
или
python -m uvicorn src.main:app --reload
``````
***
##  Команды для миграции
### 1. Инициируем алембик и создаем папку для миграций, а так же все необходимые конфиги:
``````
alembic init src/migrations
``````
### 2. Создаем миграцию:
``````
alembic revision --autogenerate -m "Будет в названии миграции"
``````
### 3. Приводим БД к последней миграции:
``````
alembic upgrade head
``````
### 4. Откат на необходимую версию
``````
alembic downgrade 2cc9735fdf6e
``````
***
##  Команды для дебага SQL-запросов
### 1. Дебажить через engine
``````
engine = create_async_engine(url=settings.DB_URL, echo=True)
``````
### 2. Дебажить через compile:
``````
async  with async_session_maker() as session:
    add_hotel_stmt = insert(HotelsORM).values(**hotel_data.model_dump())
    print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
``````
***
##  Команды docker'a
### 1. Запуск контейнера:
``````
docker compose up -d
``````
### 2 Остановка контейнера:
``````
docker compose down
``````
### 3. Просмотр запущенных контейнеров:
``````
docker ps -a
``````
***
##  Команды celery
### 1. Запуск worker в win:
``````
celery -A src.tasks.celery_app:celery_instance worker -l INFO --pool=solo
``````
### 2 Запуск beat в win:
``````
celery -A src.tasks.celery_app:celery_instance beat -l INFO
``````
### 3 Запуск worker и beat в linux/MacOS:
``````
celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B
``````
***
## Форматирование с Black по PEP8
``````
Проверка изменений
black --diff C:\Pet-projects\course_booking_hotel\src

Применение изменений в выбранной папке
black .\src\

Применение изменений для импортов
isort .\src\
``````
***
## Запуск тестов
    pytest -v

    Запуск с выводом логов 
    pytest -v

    Запуск одного теста
    pytest .\tests\integration_tests\bookings\test_api.py
*** 


