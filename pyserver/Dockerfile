FROM frolvlad/alpine-python-machinelearning:latest

RUN mkdir -p /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt
WORKDIR /usr/src/app

# Since grpc takes long time to install - specify explicitly
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python3-dev build-base \
  && apk --update add --no-cache libstdc++ \
  && pip install --upgrade pip \
  && pip install 'grpcio==1.16.1' 'grpcio-tools==1.16.1' 'protobuf==3.6.1' \
  && apk del build-dependencies

# Now install requirements
RUN pip install -r requirements.txt

EXPOSE 50051

COPY . /usr/src/app
ENTRYPOINT ["python3", "-u", "server.py"]