FROM python:3-slim

ENV BATCH_FILE "batch.csv"
ENV REQ_HEADERS {}
ENV OUTPUT_DIR .

COPY . .
RUN apt-get update && apt-get install -y build-essential --no-install-recommends \
    && pip install -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential && rm -rf /var/lib/apt/lists/*
VOLUME /data

ENTRYPOINT ["python", "main.py"]
