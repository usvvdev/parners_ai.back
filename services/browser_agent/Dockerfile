FROM python:3.12-slim

ENV OMP_NUM_THREADS=1 \
    UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=UTC \
    EASYOCR_MODULE_PATH=/models/easyocr

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# системные зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    libgl1 \
    libglib2.0-0 \
    wget \
    && rm -rf /var/lib/apt/lists/*


# =========================
# 1. УСТАНАВЛИВАЕМ TORCH ПЕРВЫМ
# =========================
RUN uv pip install --system --index-url https://download.pytorch.org/whl/cpu \
    torch==2.3.1 torchvision==0.18.1


# =========================
# 2. ЗАВИСИМОСТИ ПРОЕКТА
# =========================
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --extra browser_agent


# =========================
# 3. PLAYWRIGHT
# =========================
RUN uv run --no-sync playwright install --with-deps chromium


# =========================
# 4. КОД
# =========================
COPY libs libs/
COPY services/browser_agent services/browser_agent/


# =========================
# 5. ФИНАЛЬНАЯ СИНХРОНИЗАЦИЯ
# =========================
RUN uv sync --frozen --extra browser_agent


# =========================
# 6. PREWARM (БЕЗ CRASH EASYOCR)
# =========================
RUN python -c "import easyocr"


# =========================
# 7. START
# =========================
CMD ["uv", "run", "browser_agent"]