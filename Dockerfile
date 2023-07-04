FROM python:3.10.9-alpine

USER root

WORKDIR /backend

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY main.py .
ADD html html/
ADD json json/
ADD app app/

ENV DATABASE_LINK="mongodb://niewiem:1969v7PVDgZ7@mongo:27017/?authMechanism=DEFAULT"
ENV API_KEY="1mRI0CI84ypGOkPmy5sbSkkX1S1AjbDwCuoExuex4dmiVJyMqB"
ENV DEV="True"
ENV JWT_TOKEN="PhBH2kYqC0YNbz8j1D2lqjfIJZnIA69cabgAifRHQhY6WhloO8GLzeb1TXscHm/V"
ENV MAIL_USERNAME="no-reply@smartdorm.app"
ENV MAIL_PASSWORD="gn936GfPqYWNvTZj"
ENV API_VERSION="1"
ENV HASH_KEY="JWrZOQ5ZB-jMGVosGcsmWnzY_h00TiCr_wdlNTH5gV0="

EXPOSE 3002

CMD ["gunicorn", "-b", "0.0.0.0:3002","-w", "1", "--threads=2" ,"--certfile", "/backend/ssl/fullchain1.pem", "--keyfile", "/backend/ssl/privkey1.pem", "--capture-output", "app:app"]