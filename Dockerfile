FROM python:3.9-slim-bullseye

ADD . /app

WORKDIR /app

RUN apt-get update

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV TZ=Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


ENTRYPOINT ["python", "server.py"]
