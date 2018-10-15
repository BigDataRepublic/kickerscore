FROM python:3.6.6-alpine3.8

# Required for psycopg2 installation
RUN apk --no-cache add build-base
RUN apk --no-cache add postgresql-dev

RUN mkdir /app
RUN pip install --upgrade pip && pip install trueskill flask-restful psycopg2 flask-sqlalchemy flask-migrate flask-cors
COPY src /app

CMD ["python", "/app/app.py"]
