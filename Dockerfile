FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN apk update && apk add build-base postgresql-dev && pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]

