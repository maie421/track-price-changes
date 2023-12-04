FROM python:3.9-alpine

COPY flask/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY flask /app

WORKDIR /app

CMD ["python3", "-m", "flask", "run", "--prot=80"]