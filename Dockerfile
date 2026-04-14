FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=5000 \
    FLASK_DEBUG=0 \
    OPEN_BROWSER=0

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home appuser \
    && mkdir -p /app/app/data \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["python", "run.py"]
