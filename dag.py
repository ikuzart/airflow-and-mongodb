from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

from data import DataContainer
from data_preprocessing import BreastCancerData, BreastCancerDataLoader, BreastCancerDataPreprocessor
from mongo_wrapper import MongoClientWrapper


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'retries': 0,
    'max_active_runs': 1
}


def data_preprocessing():
    data_container = DataContainer()
    mongo_client_wrapper = MongoClientWrapper()

    data_loader = BreastCancerDataLoader()
    data_to_preprocess = BreastCancerData(data_loader)
    preproc = BreastCancerDataPreprocessor(data_to_preprocess, data_container)
    preprocessed_data = preproc.preprocess(0.3, 42)
    document_to_save = mongo_client_wrapper.make_document_from_data_container(preprocessed_data)
    mongo_client_wrapper.insert_one(document_to_save, 'test2', 'test2')

    return


def model_training():
    return 'model training'


dag = DAG('test_project', default_args=default_args)


preprocessing_operator = PythonOperator(task_id='data_preprocessing', python_callable=data_preprocessing, dag=dag)

model_training_operator = DummyOperator(task_id='model_training',  dag=dag)

preprocessing_operator >> model_training_operator
