FROM continuumio/miniconda3:4.7.10

RUN mkdir /app
COPY environment.yml /app
COPY requirements.txt /app

RUN conda update -n base -c defaults conda
RUN apt-get update \
    && apt-get install -y cmake gcc g++ make \
    && rm -rf /var/lib/apt/lists/*

RUN conda env create -f /app/environment.yml
COPY src /app

CMD ["/opt/conda/envs/kickerscore/bin/python", "/app/app.py"]
