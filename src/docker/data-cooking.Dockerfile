FROM python:3.13.5

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY src/API/ChatService/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY src/API/ChatService /app/

COPY src/docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && ls -l /entrypoint.sh

EXPOSE 5002

ENTRYPOINT ["/entrypoint.sh"]