FROM python:3

RUN pip install pika

RUN pip install requests

WORKDIR /usr/src/app

COPY consumer.py .

COPY config.json .

CMD ["python", "/usr/src/app/consumer.py"]