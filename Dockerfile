FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app/ ./app/app

CMD ["touch", "app/data/events.json", "[]"]
CMD ["chmod", "755", "app/data/events.json"]
CMD ["flask", "run", "--host=0.0.0.0"]