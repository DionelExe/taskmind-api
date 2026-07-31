FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY notification_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY notification_service ./notification_service

EXPOSE 8001

CMD ["sh", "-c", "uvicorn notification_service.main:app --host 0.0.0.0 --port ${PORT:-8001}"]
