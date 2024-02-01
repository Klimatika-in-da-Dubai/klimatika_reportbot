FROM python:3.10-alpine


RUN apk update \ 
    && apk add --no-cache gcc musl-dev python3-dev libffi-dev freetype-dev ghostscript

COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
WORKDIR /app

CMD python main.py
