import random
from faker import Faker
from sqlalchemy import text
from shapely.geometry import Point
from geoalchemy2.shape import from_shape
from sqlalchemy.sql import insert
from app.infrastructure.database.models import Building, Activity, Organization
from app.infrastructure.database.models.organization import PhoneNumber, organization_activity

from app.config.database import db_settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(
    db_settings.db_url,  # Строка подключения к базе данных
    pool_size=db_settings.POOL_SIZE,  # Размер пула соединений
    echo=db_settings.ECHO_SQL  # Включение логирования SQL-запросов
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

ACTIVITY_TREE = {
    "Продукты": {
        "Мясо": ["Колбасы", "Свинина", "Говядина"],
        "Молоко": ["Сыр", "Йогурт", "Кефир"],
        "Хлеб": ["Батон", "Бородинский"]
    },
    "Транспорт": {
        "Автомобили": ["Легковые", "Грузовые"],
        "Мотоциклы": ["Спортивные", "Чопперы"]
    },
    "Одежда": {
        "Мужская": ["Костюмы", "Джинсы"],
        "Женская": ["Платья", "Юбки"],
        "Детская": ["Шапки", "Комбинезоны"]
    }
}
fake = Faker("ru_RU")

BATCH_SIZE = 5000  # Размер батча для пакетной вставки


async def fill_fake_data():
    async with AsyncSessionLocal() as session:
        try:
            # 1️⃣ Добавляем здания (1000 штук)
            buildings = []
            for _ in range(1000):
                location = fake.location_on_land(coords_only=True)
                lat = location[0]
                lon = location[1]
                point = from_shape(Point(lon, lat), srid=4326)
                buildings.append(Building(address=fake.address(), geom=point))

            session.add_all(buildings)
            await session.commit()
            print("✅ Добавлены 1000 зданий")

            # 2️⃣ Добавляем виды деятельности (3 уровня вложенности)
            parent_map = {}  # Храним ID категорий

            for parent_name, subcategories in ACTIVITY_TREE.items():
                parent_activity = Activity(name=parent_name, parent_id=None)
                session.add(parent_activity)
                await session.flush()
                parent_map[parent_name] = parent_activity.id

                for sub_name, subsub_list in subcategories.items():
                    sub_activity = Activity(name=sub_name, parent_id=parent_activity.id)
                    session.add(sub_activity)
                    await session.flush()
                    parent_map[sub_name] = sub_activity.id

                    for subsub_name in subsub_list:
                        subsub_activity = Activity(name=subsub_name, parent_id=sub_activity.id)
                        session.add(subsub_activity)
                        await session.flush()
                        parent_map[subsub_name] = subsub_activity.id

            await session.commit()
            print("✅ Добавлены 3 уровня видов деятельности")

            # 3️⃣ Добавляем 10 000 организаций
            organizations = [
                Organization(
                    name=fake.company(),
                    building_id=random.randint(1, 1000)
                )
                for _ in range(10_000)
            ]

            for i in range(0, len(organizations), BATCH_SIZE):
                session.add_all(organizations[i:i + BATCH_SIZE])
                await session.commit()
                print(f"✅ Добавлены организации ({i + len(organizations[i:i + BATCH_SIZE])} / 10000)")

            # 4️⃣ Добавляем случайное количество телефонов (1-5 на организацию)
            phone_numbers = []
            for org_id in range(1, 10_001):
                num_phones = random.randint(1, 5)
                for _ in range(num_phones):
                    phone_numbers.append(
                        PhoneNumber(
                            number=fake.phone_number(),
                            organization_id=org_id
                        )
                    )

            for i in range(0, len(phone_numbers), BATCH_SIZE):
                session.add_all(phone_numbers[i:i + BATCH_SIZE])
                await session.commit()
                print(
                    f"✅ Добавлены номера телефонов ({i + len(phone_numbers[i:i + BATCH_SIZE])} / {len(phone_numbers)})")

            # 5️⃣ Добавляем связи "Организация ↔ Виды деятельности"
            all_activity_ids = list(parent_map.values())  # ID всех активностей
            organization_activities = []

            for org_id in range(1, 10_001):
                num_activities = random.randint(1, 3)  # Каждая компания имеет 1-3 активности
                selected_activities = random.sample(all_activity_ids, num_activities)
                for act_id in selected_activities:
                    organization_activities.append({"organization_id": org_id, "activity_id": act_id})

            for i in range(0, len(organization_activities), BATCH_SIZE):
                await session.execute(insert(organization_activity).values(organization_activities[i:i + BATCH_SIZE]))
                await session.commit()
                print(
                    f"✅ Добавлены связи Организация ↔ Виды деятельности ({i + len(organization_activities[i:i + BATCH_SIZE])} / {len(organization_activities)})")

        except Exception as e:
            print(f"❌ Ошибка: {e}")


async def clear_database():
    async with AsyncSessionLocal() as session:
        try:
            await session.execute(text("SET session_replication_role = 'replica'"))
            tables = ["phone_numbers", "organization_activity", "organizations", "activities", "buildings"]
            for table in tables:
                await session.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"))
            await session.execute(text("SET session_replication_role = 'origin'"))

            await session.commit()
            print("✅ База данных очищена!")
        except Exception as e:
            await session.rollback()
            print(f"❌ Ошибка при очистке базы: {e}")
