FROM python:3.6.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /stinerm/
COPY requirements.txt /stinerm/
WORKDIR /stinerm
RUN pip install -U pip && pip install -r requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "5", "--threads", "12", "wsgi:app"]
