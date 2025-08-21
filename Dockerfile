# ---- базовый слой ----
FROM python:3.12-slim AS base
ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=1

# ---- /bot - корневая лиректория внутри образа, можно назвать любой ----
WORKDIR /bot

# ---- deps ----
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# ---- app ----
COPY app ./app

# ---- создание директории для монтирования ----
RUN mkdir -p /bot/images

# ---- запуск ----
CMD ["python", "-m", "app.main"]
