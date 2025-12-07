FROM python:3.12

WORKDIR /app

# библиотеки для postgres + opencv
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# для web-сервиса
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
