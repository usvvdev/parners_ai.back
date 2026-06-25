FROM python:3.12-slim

ENV OMP_NUM_THREADS=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=UTC \
    EASYOCR_MODULE_PATH=/models/easyocr

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    libgl1 \
    libglib2.0-0 \
    wget \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --extra browser_agent

RUN uv run --no-sync playwright install --with-deps chromium

COPY libs libs/
COPY services/browser_agent services/browser_agent/

RUN uv sync --frozen --extra browser_agent

RUN mkdir -p /models/easyocr 

CMD ["uv", "run", "browser_agent"]