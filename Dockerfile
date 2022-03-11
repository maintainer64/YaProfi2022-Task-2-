FROM python:3.9-slim-buster
WORKDIR /opt/app
RUN apt-get update \
  && apt-get install -y libmagic-dev  \
  && apt-get clean
COPY requirements.txt .
RUN pip install --upgrade pip -r requirements.txt
COPY . .
RUN find . -name __pycache__ -type d -exec rm -rv {} +
ENV TZ=Asia/Yekaterinburg
