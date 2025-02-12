FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update
RUN apt-get install -y python3-dev gcc libc-dev libffi-dev
RUN apt-get -y install libpq-dev gcc wget

COPY ../../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY ../.. .
RUN chmod +x /app/scripts/entrypoint.sh
CMD ["/app/scripts/entrypoint.sh"]