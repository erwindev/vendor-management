FROM python:3.8-alpine

RUN adduser -D vms

WORKDIR /home/vms

COPY requirements.txt requirements.txt

RUN \
 apk update && \
 apk add --no-cache postgresql-libs libzmq && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev libffi-dev zeromq-dev && \
 pip install cython && \
 pip install psycopg2 && \
 pip install pyzmq && \
 pip install -r requirements.txt && \
 apk del .build-deps gcc musl-dev postgresql-dev libffi-dev zeromq-dev 

COPY app app
COPY migrations migrations
COPY vms_test_suite.py vms_test_suite.py
COPY vms.py vms.py
COPY run.sh run.sh
COPY .flaskenv .flaskenv
RUN chmod +x run.sh

ENV FLASK_APP vms.py

RUN chown -R vms:vms ./
USER vms

EXPOSE 5000
ENTRYPOINT ["./run.sh"]