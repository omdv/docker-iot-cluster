FROM python:3.6.4-alpine

RUN apk update

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-u", "app.py"]