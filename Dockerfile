FROM python:3.6-alpine3.6

# add ha proxy
RUN apk update
RUN apk --no-cache add haproxy

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 4444 11111 9200

CMD ["python", "start.py"]