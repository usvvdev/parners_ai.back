from pathlib import Path
from uvicorn import run
from fastapi import FastAPI
from contextlib import asynccontextmanager

from alembic.config import Config
from alembic import command

from .src.interface.api.routes import offer_router

# Определяем абсолютный путь к директории, где лежит этот скрипт
BASE_DIR = Path(__file__).parent.resolve()

# Указываем путь к папке сервиса, где лежит Alembic


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to database...")
    print("Running database migrations...")

    try:
        # Указываем пути относительно папки сервиса
        alembic_ini_path = BASE_DIR / "alembic.ini"
        migrations_dir_path = BASE_DIR / "migrations"

        # Проверяем, существуют ли файлы, чтобы избежать непонятных ошибок
        if not alembic_ini_path.exists():
            print(f"Warning: alembic.ini not found at {alembic_ini_path}")
        if not migrations_dir_path.exists():
            print(f"Warning: migrations folder not found at {migrations_dir_path}")

        alembic_cfg = Config(str(alembic_ini_path))
        alembic_cfg.set_main_option("script_location", str(migrations_dir_path))

        command.upgrade(alembic_cfg, "head")
        print("Migrations applied successfully!")

    except Exception as e:
        print(f"Error applying migrations: {e}")

    yield
    print("Cleaning up database connection...")


app = FastAPI(lifespan=lifespan)
app.include_router(offer_router)


def main():
    run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
