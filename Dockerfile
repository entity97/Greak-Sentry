FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DATA_DIR=/app/data

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /app/data

# Where the bot keeps what it has already posted. Mount a volume here so it survives restarts.
VOLUME ["/app/data"]

CMD ["python", "main.py"]
