FROM python:3.9.2-alpine

WORKDIR /root

RUN apk add build-base jpeg-dev zbar-dev rust cargo

COPY requirements.txt ./
RUN pip --disable-pip-version-check install -r requirements.txt

COPY app app
COPY main.py config.py entrypoint.sh ./

EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]
