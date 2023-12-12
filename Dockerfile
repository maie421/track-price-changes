FROM python:3.9-alpine

COPY web/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY web/cert.pem .
COPY web/key.pem .

COPY web /app

WORKDIR /app

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--cert=cert.crt", "--key=key.key"]