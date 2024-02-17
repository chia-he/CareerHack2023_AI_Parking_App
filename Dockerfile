FROM continuumio/miniconda3

WORKDIR /app

COPY . /app

RUN conda env create -f environment.yml

RUN echo "conda activate AI_Parking_App" >> ~/.bashrc
ENV PATH /opt/conda/envs/AI_Parking_App/bin:$PATH