###########
# BUILDER #
###########

# pull official base image
FROM python:3.11.4-slim-buster as builder

# set work directory
WORKDIR /usr/src/app


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# lint
RUN pip install --upgrade pip
RUN pip install flake8==6.0.0
COPY . /usr/src/app/

#RUN flake8 --ignore=E501,F401 .
RUN flake8 --ignore=E501,F401,F403 ./config

# install dependencies
#COPY ./requirements.txt .
COPY ./requirements/common.txt ./common.txt
COPY ./requirements/prod.txt ./requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.11.4-slim-buster

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME

RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles

WORKDIR $APP_HOME


# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/common.txt .
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*


## copy entrypoint.prod.sh
#COPY ./entrypoint.prod.sh .
#RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.prod.sh
#RUN chmod +x  $APP_HOME/entrypoint.prod.sh



#COPY ./compose/production/django/entrypoint.sh /entrypoint.sh
COPY ./compose/production/django/entrypoint.sh .
RUN sed -i 's/\r$//g' $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

#COPY ./compose/production/django/start.sh /start.sh
COPY ./compose/production/django/start.sh .
RUN sed -i 's/\r$//g' $APP_HOME/start.sh
RUN chmod +x  $APP_HOME/start.sh

COPY ./compose/production/django/celery/worker/start.sh ./start-celeryworker.sh
RUN sed -i 's/\r$//g' $APP_HOME/start-celeryworker.sh
RUN chmod +x  $APP_HOME/start-celeryworker.sh

COPY ./compose/production/django/celery/beat/start.sh ./start-celerybeat.sh
RUN sed -i 's/\r$//g' $APP_HOME/start-celerybeat.sh
RUN chmod +x  $APP_HOME/start-celerybeat.sh

COPY ./compose/production/django/celery/flower/start.sh ./start-flower.sh
RUN sed -i 's/\r$//g' $APP_HOME/start-flower.sh
RUN chmod +x  $APP_HOME/start-flower.sh



# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run entrypoint.prod.sh
#ENTRYPOINT ["/home/app/web/entrypoint.prod.sh"]
ENTRYPOINT ["/home/app/web/entrypoint.sh"]

