# 📌 REST API для справочника организаций, зданий и видов деятельности

## 🛠️ Стек технологий:
- **FastAPI** - для создания REST API
- **SQLAlchemy** - ORM для работы с базой данных
- **Alembic** - управление миграциями БД
- **PostgreSQL + PostGIS** - база данных с поддержкой геолокации
- **Pydantic** - валидация данных
- **Docker + Docker Compose** - для контейнеризации

---

## 📦 🔧 Как запустить проект в Docker?

### 1. **Установите Docker и Docker Compose**
Если у вас не установлен **Docker**, скачайте и установите его:  
- [📥 Скачать Docker](https://www.docker.com/get-started)

### 2. **Создайте `.env` файл**
Создайте файл **.env** в корневой папке проекта и укажите параметры подключения к базе данных:

```ini
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=organizations_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### 3. **Запуск проекта**

```bash
docker-compose up -d
```

### 4. **Дополнительные команды**

```bash
docker exec -it app python cli.py fake-data
```
```bash
docker exec -it app python cli.py clear-db
```