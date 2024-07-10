FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app/ ./app/app

CMD ["sh", "-c", "./app/script/create_event_file.sh && flask run --host=0.0.0.0 --port=5000"]