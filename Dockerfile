FROM python:3.9-alpine

RUN apk --no-cache add openssl

WORKDIR /app

COPY web/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY web /app

RUN openssl req -new -newkey rsa:4096 -x509 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/C=US/ST=YourState/L=YourCity/O=YourOrg/CN=localhost"

EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--cert=cert.pem", "--key=key.pem"]