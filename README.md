# FastAPI Микросервисы

Данный репозиторий содержит реализацию двух микросервисов на базе FastAPI: 
* TODO-сервис
* Сервис сокращения URL.

Оба сервиса используют SQLite для хранения данных и упакованы в Docker-контейнеры.

## Запуск сервисов локально

### Шаги по запуску

1. Клонируем репозиторий:

    ```git clone <URL_данного_репозитория> cd FastAPI_HSE_API```

2. Находясь в директории нашего проекта запускаем Docker Compose (3 команды для разных целей):  
- Сборка образов:  
    ```sudo docker-compose up --build```  
- Сборка образов без использования кэшированных слоев:  
    ```sudo docker-compose build --no-cache```  
- Сборка с принудительным пересозданием томов:  
    ```sudo docker-compose up --build --force-recreate```

  После выполнения команды должны увидеть подобный вывод:
  ![Иллюстрация к проекту № 1](https://github.com/MaxKots/FastAPI_HSE_API/blob/main/.assets/1.png)


**Теперь сервисы доступны по адресу:**  
    TODO-сервис:  
    ```http://localhost:8000/docs```  
    <br>
    Сервис сокращения URL:  
    ```http://localhost:8001/docs```

### Эндпоинты
TODO-сервис:

    POST /items/: Создание задачи
    GET /items/: Получение списка задач
    GET /items/{item_id}: Получение задачи по ID
    PUT /items/{item_id}: Обновление задачи по ID
    DELETE /items/{item_id}: Удаление задачи
    DELETE /items/: Удаление всех задач

  ![Иллюстрация к проекту № 2](https://github.com/MaxKots/FastAPI_HSE_API/blob/main/.assets/2.png)
**Сервис сокращения URL:**

    POST /shorten/: Создание короткой ссылки
    GET /{short_id}: Перенаправление на полный URL
    GET /stats/{short_id}: Отображение сведений по URL
    
  ![Иллюстрация к проекту № 3](https://github.com/MaxKots/FastAPI_HSE_API/blob/main/.assets/3.png)


  ### Примеры Curl- запросов для проверки работы сервиса:  
  **Создание экземпляра:**  
```
curl -X 'POST' \
  'http://localhost:8000/items/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 0,
  "title": "Экземпляр №1",
  "description": "Тестовый вариант",
  "completed": false
}'
```

**Ответ:**  
```
{"id":2,"title":"Экземпляр №1","description":"Тестовый вариант","completed":false}
```

**Вывод экземпляров:**  
```
curl -X 'GET' \
  'http://localhost:8000/items/' \
  -H 'accept: application/json'
```

**Ответ:** 
```
[{"id":1,"title":"Экземпляр №1","description":"Тестовый вариант","completed":false},{"id":2,"title":"Экземпляр №1","description":"Тестовый вариант","completed":false}]
```

**Удаление всех экземпляров:**  
```
curl -X 'DELETE' \
  'http://localhost:8000/items/' \
  -H 'accept: application/json'
```

**Ответ:**
```
{"message":"All items deleted"}
```
  
___

### Additives & troubleshooting

Для остановки работы рекомендую команду:  
   ```docker stop $(docker ps -a -q)```
   
Для удаления образов и перезапуска докер используем команды:  
   ```docker rmi -f docker.io/library/fastapi_hse_api_todo_service```  
   ```docker rmi -f docker.io/library/fastapi_hse_api_shorturl_service```  
   ```sudo systemctl restart docker```  

Для отображения томов используем команду:  
   ```docker volume ls```  
Для удаления всех неиспользуемых томов используем:  
   ```docker volume prune```  

Прежде чем пытаться удалять тома, нужно полностью удалить все контейнеры, которые могли их использовать, так как демоны могут взаимодействовать с томами даже после остановки контейнера:  
Выведем контейнеры:  
   ```docker ps -a```  
удалим интересующий нас контейнер:  
   ```docker rm -f <id_контейнера>```  
удалим тома:  
   ```docker volume rm fastapi_hse_api_todo_data```  
   ```docker volume rm fastapi_hse_api_shorturl_data```  


Сборка образов выполнялась следующими командами:  
``` docker build -t <ваш_логин_hub>/todo-service:latest todo_app/```
``` docker build -t <ваш_логин_hub>/shorturl-service:latest shorturl_app/```  

Авторизуемся в Docker Hub командой:  
 ```docker login```  
 
Выполняем отправку образов в удаленный репозиторий Docker Hub:  
 ```docker push <ваш_логин_hub>/todo-service:latest```  
 ```docker push <ваш_логин_hub>/shorturl-service:latest```  

**Ошибка:**
Если при попытке выполнить ```docker login``` видим:  
   ```Error saving credentials: error storing credentials - err: exec: "docker-credential-desktop": executable file not found in $PATH, out: ''```    
Убеждаемся, что у нас есть учетная запись в Docker Hub и в Account Settings создан Personal access token

Выполняем в терминале:   
   ```sudo vi ~/.docker/config.json```  
И меняем credsStore на credStore, после данной процедуры авторизация в Docker Hub через командную строку рабоатет и нам удается войти через учетную запись GitHub.

**HOTFIX:**  
Добавлено использование AUTOINCREMENT в SQL: При создании таблицы id задачи будет автоматически увеличиваться.  
Исправление метода create_item: Метод теперь возвращает элемент с его id после добавления.  
Добавление маршрута для удаления всех элементов: Новый маршрут DELETE /items/ позволяет удалить все элементы из базы данных.  





