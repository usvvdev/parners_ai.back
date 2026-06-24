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


FROM python:3.12-slim

# Установка uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# УБРАЛИ UV_LINK_MODE=copy ! Это раздувало образ и тормозило сохранение.
ENV UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=UTC

WORKDIR /app

# 1. Конфиги
COPY pyproject.toml uv.lock ./

# 2. ТОЛЬКО libs (если они нужны для резолвинга зависимостей в pyproject.toml)
COPY libs libs/

# 3. Кэшируем САМИ ЗАГРУЗКИ пакетов (чтобы не качать заново при смене версии)
# И ставим внешние зависимости
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --extra browser_agent

# 4. Playwright. ОБЯЗАТЕЛЬНО --with-deps, иначе не запустится!
RUN uv run --no-sync playwright install --with-deps chromium

# 5. КОД КОПИРУЕМ САМЫМ ПОСЛЕДНИМ.
# Теперь изменение кода не будет сбрасывать кэш шагов 3 и 4!
COPY services/browser_agent services/browser_agent/

# 6. Финальная установка проекта (отработает за 1-2 секунды)
RUN uv sync --frozen --extra browser_agent

CMD ["uv", "run", "browser_agent"]