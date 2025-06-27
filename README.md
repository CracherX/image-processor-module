
# Image-processor-module

Веб-приложение для обработки изображений.

---

## Описание

Сервис позволяет составлять очередь обработки изображений.   

## Запуск приложения

### Через Docker Compose

```bash
docker-compose up --build
```

Это запустит сервис с необходимой базой данных, брокером сообщений и приложением.

---

## Конфигурация

### config.yaml

```yaml
app_host: "0.0.0.0"
app_port: 80

pg:
  host: "db_tasks"
  port: 5432
  user: "test"
  password: "123"
  database: "test_tasks"

logging:
  root_log_level: 10
  modules:
    - name: pika
      log_level: 30

filer:
  url: "http://filer:80"
  connect_timeout: 3
  read_timeout: 15
  auto_comment: "Изображение было автоматически обработано"
  server_save_path: ""

rabbit:
  host: rabbit
  port: 5672
  user: test
  password: test
  routing_key: tasks
  queue_name: tasks

upload_dir: "/uploads"
```

### Переменные окружения (опциональные)

* YAML_PATH=/config.yaml
* APP_HOST=0.0.0.0
* APP_PORT=80
* UPLOAD_DIR=/uploads

---

## Основные маршруты API

### Получить список задач

```
POST /api/tasks/task/
```
- Создаёт новую задачу по обработке.
- Если алгоритм указан не правильно, вам вернёт 400 и список допустимых значений в data.
- Возможные params для SCALING: scale_x(int), scale_y(int)
- Возможные params для PROJECTION: target_projection(str)
- Ключи тела запроса:

| Параметр  | Тип    | Описание                           | По умолчанию |
|-----------|--------|------------------------------------|--------------|
| file_id   | int    | ID файла из файлового сервиса      | Обязателен   |
| algorithm | string | SCALING/PROJECTION                 | Обязателен   |
| params    | объект | Дополнительные параметры обработки | Отсутствуют  |

---

### Получить информацию о задаче

```
GET /api/tasks/task/<int:task_id>/
```

- Возвращает информацию о задаче по её ID.

---

### Получить список задач

```
GET /api/tasks/
```

- Получить весь список задач.

---

