import json
import os
import pickle
from typing import Any, Dict, Tuple

from data import DataContainer

import numpy as np
import pandas as pd
from pymongo import MongoClient
from sklearn.ensemble import RandomForestClassifier
from bson.objectid import ObjectId
from bson.binary import Binary

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')


class MongoClientWrapper:

    def __init__(self):
        self.client = MongoClient(MONGO_URI)

    def insert_one(self, document: Dict[str, Any], db: str, collection: str) -> str:
        db_ = self.client[db]
        id_ = db_[collection].insert_one(document)
        return id_

    def find_by_id(self, id_: str, db: str, collection: str) -> Dict[str, Any]:
        db_ = self.client[db]
        document = db_[collection].find_one({"_id": ObjectId(id_)})
        return document

    def update_one(self, id_: str, db: str, collection: str, document_to_save: Dict[str, Any]):
        db_ = self.client[db]
        db_[collection].update_one({"_id": ObjectId(id_)}, {"$set": document_to_save}, upsert=True)



    @staticmethod
    def make_document_from_data_container(data_container: DataContainer) -> Dict[str, Any]:
        documents_to_save = {}
        for attr in dir(data_container):
            if attr.startswith('__'):
                continue
            attr_value = data_container.__getattribute__(attr)
            if isinstance(attr_value, pd.DataFrame):
                attr_value = json.loads(attr_value.T.to_json())
            elif isinstance(attr_value, pd.Series):
                attr_value = json.loads(attr_value.to_json())
            elif isinstance(attr_value, np.ndarray):
                attr_value = attr_value.tolist()
            elif isinstance(attr_value, RandomForestClassifier):
                attr_value = Binary(pickle.dumps(attr_value))
            documents_to_save[attr] = attr_value

        return documents_to_save

    @staticmethod
    def get_train_test_data_from_document(document: Dict[str, Any]) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        return pd.DataFrame(document["X_train"]).T, \
               pd.DataFrame(document["X_test"]).T, \
               pd.Series(document["y_train"]), \
               pd.Series(document["y_test"])
