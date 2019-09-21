FROM continuumio/miniconda3:4.7.10

RUN mkdir /app
COPY environment.yml /app
COPY requirements.txt /app

RUN apt-get update \
    && apt-get install -y cmake gcc g++ make \
    && rm -rf /var/lib/apt/lists/*

RUN conda env create -f /app/environment.yml

# Prevent pip from compiling dlib which takes ages
RUN /opt/conda/envs/kickerscore/bin/pip install face_recognition==1.2.3 face_recognition_models==0.3.0 --no-deps

COPY src /app

RUN ln -sf /opt/conda/envs/kickerscore/bin/python /opt/conda/bin/python

CMD ["python", "/app/app.py"]
