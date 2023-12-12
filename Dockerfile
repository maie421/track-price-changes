FROM python:3.9-alpine

COPY ssl/ /etc/ssl/

COPY web/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY web /app

WORKDIR /app

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--cert=/etc/ssl/certificate.crt", "--key=/etc/ssl/private.key"]