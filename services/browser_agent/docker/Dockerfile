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

# Установка uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Оптимизации
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TZ=UTC

WORKDIR /app

# 1. Сначала только конфиги зависимостей
COPY pyproject.toml uv.lock ./

# 2. Копируем ТОЛЬКО libs (как ты попросил)
COPY libs libs/
COPY services/browser_agent services/browser_agent/

# 3. Ставим зависимости (без проекта ещё)
RUN uv sync --frozen --no-install-project --extra browser_agent

# 4. Playwright (без --with-deps чтобы не раздувать образ)
RUN uv run --no-sync playwright install chromium

# 5. Теперь ставим сам проект
RUN uv sync --frozen --extra browser_agent

# 6. Запуск
CMD ["uv", "run", "browser_agent"]