FROM alpine

RUN apk update \
 && apk add gcc python3-dev libtool libc-dev libpostal-dev py3-pip libpostal-data \
 && pip install --break-system-packages geopy postal pandas

COPY . .
ENV PYTHONUNBUFFERED 1
CMD ["python3", "run.py"]