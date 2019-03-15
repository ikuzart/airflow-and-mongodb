import os
from datetime import datetime
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
APP_LOG_FILE = os.getenv('APP_LOG_FILE', 'main.log')
TEST_SIZE = os.getenv('TEST_SIZE', 0.3)
RANDOM_STATE = os.getenv('RANDOM_STATE', 42)
MONGO_DB = os.getenv('MONGO_DB', 'test_db')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'test_collection')

default_args = {
    'owner': os.getenv('OWNER', 'airflow'),
    'depends_on_past': os.getenv('DEPEDN_ON_PAST', False),
    'start_date': os.getenv('START_DATE', datetime(2015, 6, 1)),
    'retries': os.getenv("RETRIES", 1),
    'max_active_runs': os.getenv('MAX_ACTIVE_RUNS', 1)
}

if not os.path.exists(APP_LOG_FILE):
    APP_LOG_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), APP_LOG_FILE)

log_config = {
    'version': 1,
    'formatters': {
        'default': {'format': '%(asctime)s - %(levelname)s - %(message)s', 'datefmt': '%Y-%m-%d %H:%M:%S'}
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': APP_LOG_FILE
        }
    },
    'loggers': {
        'default': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    },
    'disable_existing_loggers': False
}
