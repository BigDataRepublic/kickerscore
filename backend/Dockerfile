FROM continuumio/miniconda3

RUN mkdir /opt/app
RUN apt-get update && apt-get install -y libpq-dev && apt-get clean
RUN pip install --upgrade pip && pip install trueskill flask-restful psycopg2
COPY src /opt/app

CMD ["python", "/opt/app/server.py"]
