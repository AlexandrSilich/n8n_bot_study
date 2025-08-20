# ---- базовый слой ----
FROM python:3.12-slim AS base
ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=1

WORKDIR /bot

# ---- deps ----
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# ---- app ----
COPY app ./app

# ---- запуск ----
CMD ["python", "-m", "app.main"]
