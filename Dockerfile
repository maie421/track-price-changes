FROM python:3.9-alpine

RUN apt-get update \
 && apt-get install -y tk tcl

RUN pip install --upgrade pip \
 && pip install -e . \

COPY web/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY web /app

WORKDIR /app

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]