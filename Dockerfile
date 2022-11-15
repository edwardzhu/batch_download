FROM python:3-slim

ENV BATCH_FILE "batch.csv"
ENV REQ_HEADERS {}
ENV OUTPUT_DIR .

COPY . .
RUN pip install -r requirements.txt
VOLUME /data

ENTRYPOINT ["python", "main.py"]
