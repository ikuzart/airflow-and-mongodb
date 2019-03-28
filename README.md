# Apache Airflow DAG's to save ML model in MongoDB
To build and run mongo and airflow app with docker 
```
docker-compose up
```
MongoDB will be available on mongodb://localhost:27017/
Airflow will be avilable on http://localhost:27017/

To trigger DAG:
```
docker exec app airflow trigger_dag test_project
```

Environment variables for configuration
```
export AIRFLOW_HOME=~/airflow
export MONGO_URI=mongodb://localhost:27017/
```

files from dags/ need to be copied to  ${AIRFLOW_HOME}/dags

To run
```
python main.py
```


