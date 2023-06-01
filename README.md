# Блокнот
## что сделано


- модель заметки
    - id 
    - ФИО друга
    - дата рождения
    - пожелание подарка
- API
    - добавление
    - редактирование
    - удаление
    - отображение всех записей
- dockerfile
- docker-compose
- файл с зависимостями
- проект опубликован на github

## как запустить
1) Удаляем все образы
 ```
 docker rm -f <ID>
 docker system prune
 docker system prune -
 ```

2) Поднимем docker-compose и проверим что он собирается
```
docker-compose up --build -d
```

3) Проверяем что всё работает
4) Проверяем логи docker-compose
```
docker-compose logs
```

## Тест через postman

программа запускается на localhost
ниже адрес с методом и примером

GET
```http://localhost```

POST
```http://localhost/post```

```
{
    "name": "ahmed",
    "date": "11.11.12",
    "wish": "ps54"
}
```
PUT
```http://localhost/put/1```

```
{
    "name": "ahmed1",
    "date": "10.10.12",
    "wish": "ps"
}
```
DELETE
```http://localhost/delete/1```
