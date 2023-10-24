FROM python:3.10
RUN pip install uwsgi
WORKDIR /app


ADD . /app
RUN pip install -r requirements.txt

CMD ["uwsgi", "app.ini"]


