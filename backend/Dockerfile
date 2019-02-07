FROM python:3.6.6-alpine3.8

# Required for psycopg2 installation
RUN apk --no-cache add build-base
RUN apk --no-cache add postgresql-dev

RUN mkdir /app
COPY requirements.txt /app

# For some reason we need to install numpy BEFORE installing pandas
RUN pip install numpy==1.16.0
RUN pip install -r /app/requirements.txt
COPY src /app

CMD ["python", "/app/app.py"]
