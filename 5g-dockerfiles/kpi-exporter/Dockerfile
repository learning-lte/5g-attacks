FROM python:3.8-slim
LABEL maintainer="Niloy Saha <niloysaha.ns@gmail.com>"
LABEL description="Slice KPI Exporter v1.0.0"


RUN mkdir -p /exporter/

WORKDIR /exporter
COPY /app/requirements.txt ./
RUN pip install -r requirements.txt
COPY /app/* ./

EXPOSE 9000

CMD python3 kpi-exporter.py