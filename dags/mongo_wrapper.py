import json
import os
from typing import Any, Dict

from data import DataContainer

import pandas as pd
from pymongo import MongoClient

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')


class MongoClientWrapper:

    def __init__(self):
        self.client = MongoClient(MONGO_URI)

    def insert_one(self, document, db, collection):
        db_ = self.client[db]
        collection_ = db_[collection]
        _id = collection_.insert_one(document)
        return _id

    def make_document_from_data_container(self, data_container: DataContainer) -> Dict[str, Any]:
        documents_to_save = {}
        for attr in dir(data_container):
            if attr.startswith('__'):
                continue
            attr_value = data_container.__getattribute__(attr)
            if isinstance(attr_value, pd.DataFrame):
                attr_value = json.loads(attr_value.T.to_json())
            elif isinstance(attr_value, pd.Series):
                attr_value = json.loads(attr_value.to_json())
            documents_to_save[attr] = attr_value

        return documents_to_save
