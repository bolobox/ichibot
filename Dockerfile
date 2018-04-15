FROM python:2

RUN mkdir /usr/local/ichibot/
WORKDIR /usr/local/ichibot/

COPY app/requirements.txt /usr/local/ichibot/requirements.txt
RUN pip install -r requirements.txt

COPY app /usr/local/ichibot/


CMD python live-ichi.py
