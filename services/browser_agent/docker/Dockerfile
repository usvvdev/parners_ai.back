# FROM python:3.12-slim

# # 1. Установка uv
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# # Оптимизации для Docker
# ENV UV_COMPILE_BYTECODE=1
# ENV UV_LINK_MODE=copy

# WORKDIR /app

# # 2. Копируем файлы конфигурации проекта
# COPY pyproject.toml uv.lock ./

# # 3. Синхронизируем ТОЛЬКО внешние зависимости для browser-agent
# # --extra browser-agent указывает uv установить эту конкретную группу
# RUN uv sync --frozen --no-install-project --extra browser_agent

# # 4. Устанавливаем системные зависимости Playwright и Chromium
# # Пакет playwright уже скачан на предыдущем шаге, uv run задействует его
# RUN uv run --no-sync playwright install --with-deps chromium

# # 5. Копируем весь исходный код (включая папки libs и services)
# COPY libs libs/
# COPY services/browser_agent services/browser_agent/

# # 6. Финальный sync — теперь uv устанавливает сам проект (ваши пакеты)
# # и регистрирует скрипт [project.scripts] browser_agent
# RUN uv sync --frozen --extra browser_agent

# RUN uv run --no-sync playwright install --with-deps chromium

# # 7. Запуск сервиса через зарегистрированный скрипт проекта
# CMD ["uv", "run", "browser_agent"]


FROM python:3.12-slim AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --extra browser_agent

FROM python:3.12-slim

COPY --from=base /app /app
COPY --from=base /root/.cache /root/.cache

RUN uv run --no-sync playwright install chromium

CMD ["uv", "run", "browser_agent"]