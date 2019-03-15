from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

from data import DataContainer
from data_preprocessing import BreastCancerData, BreastCancerDataLoader, BreastCancerDataPreprocessor
from mongo_wrapper import MongoClientWrapper
from settings import TEST_SIZE, RANDOM_STATE, MONGO_DB, MONGO_COLLECTION, default_args


def data_preprocessing():
    data_container = DataContainer()
    mongo_client_wrapper = MongoClientWrapper()

    data_loader = BreastCancerDataLoader()
    data_to_preprocess = BreastCancerData(data_loader)
    preproc = BreastCancerDataPreprocessor(data_to_preprocess, data_container)
    preprocessed_data = preproc.preprocess(TEST_SIZE, RANDOM_STATE)
    document_to_save = mongo_client_wrapper.make_document_from_data_container(preprocessed_data)
    mongo_client_wrapper.insert_one(document_to_save, MONGO_DB, MONGO_COLLECTION)

    return


def model_training():
    return 'model training'


dag = DAG('test_project', default_args=default_args, schedule_interval=None)


preprocessing_operator = PythonOperator(task_id='data_preprocessing', python_callable=data_preprocessing, dag=dag)

model_training_operator = DummyOperator(task_id='model_training',  dag=dag)

preprocessing_operator >> model_training_operator
