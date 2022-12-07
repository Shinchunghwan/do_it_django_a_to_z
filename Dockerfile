# 도커 파이썬에서 설치되어있는 이미지 불러옴
from python:3.10.8-slim-buster

# 프로젝트 작업을 usr/src/app 으로 지정
WORKDIR /usr/src/app


#
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERD 1

COPY . /usr/src/app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

