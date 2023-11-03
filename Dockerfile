FROM python:3.11-slim
WORKDIR /src
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY app/ ./app
CMD gunicorn -b 0.0.0.0:8000 app:app