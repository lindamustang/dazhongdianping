from python:3.7.4-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# RUN pip install scrapy

COPY . .

ENTRYPOINT [ "python" ]



