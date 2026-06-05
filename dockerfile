# dockerfile contains the sequential list of instructions that tell docker what kind of container image it needs to build
ARG AIRFLOW_VERSION=2.9.2
ARG PYTHON_VERSION=3.10

# Setting up the specific image with the mentioned versions
FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION} 

# Creating the path 
ENV AIRFLOW_HOME=/opt/airflow

# Bringing in the req.txt file into the dockerimage
COPY requirements.txt /

# Building the image
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt