FROM --platform=linux/arm/v7 ubuntu:jammy as build
FROM python:3.11-slim
LABEL Maintainer="lavron.dev"
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY src .
CMD ["python", "src/main.py"]