FROM python:3-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/bot/main.py"]