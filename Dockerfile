FROM python:3.6.8

RUN apt-get update && apt-get install -y supervisor gcc
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV AIRFLOW_HOME=/app/airflow
ENV SLUGIFY_USES_TEXT_UNIDECODE=yes
ENV MONGO_URI=mongo:27017
RUN pip install apache-airflow pandas pymongo scikit-learn python-dotenv
COPY /dags/. $AIRFLOW_HOME/dags/

RUN airflow initdb

EXPOSE 8080

CMD ["/usr/bin/supervisord"]
