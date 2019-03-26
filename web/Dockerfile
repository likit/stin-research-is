FROM python:3.6.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /project_root/
COPY requirements.txt /project_root/
WORKDIR /project_root
RUN pip install -U pip && pip install -r requirements.txt
