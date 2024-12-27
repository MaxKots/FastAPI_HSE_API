# FastAPI Microservices

Этот проект реализует два микросервиса на базе FastAPI: TODO-сервис и сервис сокращения URL. Оба сервиса используют SQLite для хранения данных и упакованы в Docker-контейнеры.

## Запуск сервисов локально

### Требования
- Docker
- Docker Compose

### Шаги по запуску

1. Клонируйте репозиторий:

   ```bash
   git clone <URL_репозитория>
   cd FastAPI_HSE_API

    Запустите Docker Compose:

     
    sudo docker-compose up --build
ИЛИ, если нам требуется пересоздать тома:
    sudo docker-compose build --no-cache
Принудлительное пересоздание томов:
нихера не пашет    sudo docker-compose up --build --force-recreate



    TODO-сервис доступен по адресу:
    http://localhost:8000/docs

    Сервис сокращения URL доступен по адресу:
    http://localhost:8001/docs

Эндпоинты
TODO-сервис

    POST /items/: Создание задачи
    GET /items/: Получение списка задач
    GET /items/{item_id}: Получение задачи по ID
    PUT /items/{item_id}: Обновление задачи по ID
    DELETE /items/{item_id}: Удаление задачи

Сервис сокращения URL

    POST /shorten/: Создание короткой ссылки
    GET /{short_id}: Перенаправление на полный URL


После завершения работы контейнеров, их можно запустить командой:
Для TODO_service:
    docker start 34f1fb0fd8ed
Для Shortener_url:
    docker start 59bda0fe2b1c


Иногда полезн овыполнить рестарт докера:
docker rmi -f docker.io/library/fastapi_hse_api_todo_service
docker rmi -f docker.io/library/fastapi_hse_api_shorturl_service


sudo systemctl restart docker

показатьь тома:
docker volume ls
удалить все неиспользуемые тома:
docker volume prune

HOTFIX:
Использование AUTOINCREMENT в SQL: При создании таблицы id будет автоматически увеличиваться.
Исправление метода create_item: Метод теперь возвращает элемент с его id после добавления.
Добавление маршрута для удаления всех элементов: Новый маршрут DELETE /items/ позволяет удалить все элементы из базы данных.

Остановить все контейнеры
docker stop $(docker ps -a -q)

преждче чем удалять тома, нужно полностью удалить все контейнеры, которые могли их использовать, так как демоны могут взаимодействовать с томами даже после отключения конетйнера:
docker ps -a
docker rm -f 0f31cba4bbd3

и только потом удалять тома:
docker volume rm fastapi_hse_api_todo_data





