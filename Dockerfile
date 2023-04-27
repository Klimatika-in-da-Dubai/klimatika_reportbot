FROM python:3.10-alpine

COPY . /app
WORKDIR /app

RUN apk update \ 
    && apk add --no-cache gcc musl-dev python3-dev libffi-dev freetype-dev ghostscript

RUN pip install --no-cache-dir -r requirements.txt

CMD python main.py
