# pull the official base image
FROM python:3.7.3-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --virtual build-deps gcc python-dev musl-dev \
    && apk add --no-cache mariadb-dev

RUN pip install mysqlclient==1.4.6  

RUN apk del build-deps

# install dependencies
RUN pip install --upgrade pip 
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]