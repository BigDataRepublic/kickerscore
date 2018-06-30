FROM continuumio/miniconda3

RUN mkdir /opt/app
RUN pip install --upgrade pip && pip install trueskill flask-restful
COPY src /opt/app

CMD ["python", "/opt/app/server.py"]
