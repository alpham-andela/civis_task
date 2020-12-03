FROM python:3.8

COPY requirements.txt /
RUN python -m pip install --upgrade pip
RUN python -m pip install -r /requirements.txt
RUN rm requirements.txt


WORKDIR /usr/src/app/

COPY . /usr/src/app

CMD python ./hubspot_etl.py