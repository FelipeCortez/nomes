FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

ADD requirements.txt /code/

RUN apk update && \
 python3 -m pip install -r requirements.txt --no-cache-dir

ADD . /code/

ENTRYPOINT ["python"]

CMD ["api.py"]
