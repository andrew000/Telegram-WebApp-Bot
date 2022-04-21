FROM python:3.9.12-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc

COPY ./requirements.txt requirements.txt

RUN pip install --user -r requirements.txt


FROM python:3.9.12-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ENV PATH=/root/.local/bin:$PATH
COPY --from=builder /root/.local /root/.local

COPY . .
