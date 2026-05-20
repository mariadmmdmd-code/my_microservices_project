FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV RATINGS_API_URL=http://ratings_api:8002

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]