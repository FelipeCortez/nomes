FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV development

RUN mkdir /code

WORKDIR /code

ADD . /code/

RUN apk update \
    && python3 -m pip install -r requirements.txt --no-cache-dir \
    && apk add gcc musl-dev make sqlite sqlite-dev pkgconfig \
    && cd SQLite-Levenshtein && ./configure && make \
    && cd .. && cp SQLite-Levenshtein/src/.libs/liblevenshtein.so .

ENTRYPOINT ["python"]

CMD ["api.py"]
