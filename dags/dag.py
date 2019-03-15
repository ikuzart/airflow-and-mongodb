from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from data import DataContainer
from data_preprocessing import BreastCancerData, BreastCancerDataLoader, BreastCancerDataPreprocessor
from model_building import ModelBuilder
from mongo_wrapper import MongoClientWrapper
from settings import TEST_SIZE, RANDOM_STATE, MONGO_DB, MONGO_COLLECTION, default_args


def data_preprocessing(**kwargs):
    data_container = DataContainer()
    mongo_client_wrapper = MongoClientWrapper()

    data_loader = BreastCancerDataLoader()
    data_to_preprocess = BreastCancerData(data_loader)
    preproc = BreastCancerDataPreprocessor(data_to_preprocess, data_container)
    preprocessed_data = preproc.preprocess(TEST_SIZE, RANDOM_STATE)
    document_to_save = mongo_client_wrapper.make_document_from_data_container(preprocessed_data)
    id_ = mongo_client_wrapper.insert_one(document_to_save, MONGO_DB, MONGO_COLLECTION)
    return id_.inserted_id


def model_training(**kwargs):
    ti = kwargs['task_instance']
    id_ = ti.xcom_pull(task_ids='data_preprocessing')
    print(id_)
    mongo_client_wrapper = MongoClientWrapper()
    data_container = DataContainer()

    document = mongo_client_wrapper.find_by_id(id_,  MONGO_DB, MONGO_COLLECTION)
    print(document)
    model_builder = ModelBuilder(*mongo_client_wrapper.get_train_test_data_from_document(document))
    data_container.classifier = model_builder.build_classifier()
    data_container.prediction = model_builder.prediction(data_container.classifier)
    data_container.metrics = model_builder.get_metrics(data_container.prediction)
    document_to_save = mongo_client_wrapper.make_document_from_data_container(data_container)

    mongo_client_wrapper.update_one(id_, MONGO_DB, MONGO_COLLECTION, document_to_save)


dag = DAG('test_project', default_args=default_args, schedule_interval=None)


preprocessing_operator = PythonOperator(task_id='data_preprocessing',
                                        python_callable=data_preprocessing,
                                        provide_context=True,
                                        dag=dag)

model_training_operator = PythonOperator(task_id='model_training',
                                         provide_context=True,
                                         python_callable=model_training,
                                         dag=dag)

preprocessing_operator >> model_training_operator
