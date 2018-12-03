FROM python:3.7.1-alpine3.7

RUN mkdir -p /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt
WORKDIR /usr/src/app

RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python3-dev build-base \
  && apk --update add --no-cache libstdc++ \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  && apk del build-dependencies

# Compile proto
# COPY api.proto /usr/src/app/api.proto
# RUN python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. api.proto

EXPOSE 50051

COPY . /usr/src/app
ENTRYPOINT ["python3", "-u", "server.py"]