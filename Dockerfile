FROM python:3.9.12-buster

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt

COPY config.yaml /usr/src/app

COPY el2datalake.py /usr/src/app
RUN chmod a+x el2datalake.py

CMD ["./el2datalake.py"]
