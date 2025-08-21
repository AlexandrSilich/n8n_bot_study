FROM python:3.12-slim AS base
ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=1

WORKDIR /bot

COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

COPY app ./app
COPY logo.jpg ./app/logo.jpg  # если нужен файл логотипа

CMD ["python", "-m", "app.main"]
