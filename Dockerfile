FROM python:3.9

COPY web/requirements.txt requirements.txt

RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY web /app

WORKDIR /app

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]