FROM python:3.9

WORKDIR /app

ADD . /app

RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uwsgi","uwsgi.ini"]