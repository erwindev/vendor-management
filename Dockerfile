FROM python:3.7-alpine

RUN adduser -D vms

WORKDIR /home/vms

COPY requirements.txt requirements.txt
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
 && pip install cython \
 && pip install -r requirements.txt --default-timeout=100 future \
 && apk del .build-deps

COPY app app
COPY migrations migrations
COPY vms.py vms.py
COPY run.sh run.sh
COPY .flaskenv .flaskenv
COPY .env .env
RUN chmod +x run.sh

ENV FLASK_APP vms.py

RUN chown -R vms:vms ./
USER vms

EXPOSE 5000
ENTRYPOINT ["./run.sh"]