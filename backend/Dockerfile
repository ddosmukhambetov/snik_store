FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip --no-warn-script-location
RUN pip install -r requirements.txt --no-cache-dir --no-warn-script-location

COPY . .