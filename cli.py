from app.infrastructure.cli.fixture import clear_database, fill_fake_data
import typer
import asyncio

# Создаем экземпляр приложения Typer
app = typer.Typer()


# Команда для очистки базы данных
@app.command()
def fake_data():
    """Очистить базу данных"""
    asyncio.run(fill_fake_data())


@app.command()
def clear_db():
    """Очистить базу данных 2"""
    asyncio.run(clear_database())


if __name__ == "__main__":
    app()
