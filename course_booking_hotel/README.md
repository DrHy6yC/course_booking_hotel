# Полезные команды
***
## Связывание локального Git'а и GitHub
```git remote add main https://github.com/DrHy6yC/course_booking_hotel.git ```
***
## Активация виртуального окружения
```. venv/bin/activate ```
***
##  Запуск проекта
```python src/main.py```
***
## Работа с внешними библиотеками
### 1. Установка библиотек из requirements.txt
```pip install -r requirements.txt ```
### 2. Добавление установленных библиотек в requirements.txt
```pip freeze >requirements.txt```
***
##  Команды для миграции
### 1. Инициируем алембик и создаем папку для миграций, а так же все необходимые конфиги:
```alembic init src/migrations```
### 2. Создаем миграцию:
```alembic revision --autogenerate -m "Будет в названии миграции"```
### 3. Приводим БД к последней миграции:
```alembic upgrade head```
### 4. Откат на необходимую версию
```alembic downgrade 2cc9735fdf6e ```
***
##  Команды docker'a
### 1. Запуск контейнера:
```docker compose up -d```
### 2 Остановка контейнера:
```docker compose down```
### 3. Просмотр запущенных контейнеров:
```docker ps -a```
***


