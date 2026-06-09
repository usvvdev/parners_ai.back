FROM python:3.12-slim

# 1. Установка uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Оптимизации для Docker
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

# 2. Копируем файлы конфигурации проекта
COPY pyproject.toml uv.lock ./

# 3. Синхронизируем ТОЛЬКО внешние зависимости для bot
# --extra browser-agent указывает uv установить эту конкретную группу
RUN uv sync --frozen --no-install-project --extra api

# 4. Копируем весь исходный код (включая папки libs и services/bot)
COPY libs libs/
COPY services/bot services/bot/

# 5. Финальный sync — теперь uv устанавливает сам проект (ваши пакеты)
# и регистрирует скрипт [project.scripts] bot
RUN uv sync --frozen --extra bot

# 6. Запуск сервиса через зарегистрированный скрипт проекта
CMD ["uv", "run", "bot"]