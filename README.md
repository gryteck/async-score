Перед запуском создать файл с переменными окружениями

```bash
cp .env.example .env
```

Собрать контейнеры
```bash
docker compose build
```

Поднять собранные контейнеры
```bash
docker compose up -d
```

- UI `Kafka` будет доступна по адресу http://localhost:8090
- `Бэкенд` будет доступен по адресу http://localhost:8081/docs
- База данных `postgres` будет доступен по порту `5432`
