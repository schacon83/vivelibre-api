# Parent image
FROM python:3.12

# Se incluye para hora de los logs
ENV TZ="Europe/Madrid"

ARG VERSION
ENV VERSION=$VERSION

# Install needed libs
RUN apt update && apt install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app
RUN chmod +x /app/entrypoint.sh

EXPOSE 8008
ENTRYPOINT ["./entrypoint.sh"]
