from collections import OrderedDict
from typing import NamedTuple

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, roc_auc_score, f1_score

from settings import CRITERION, N_ESTIMATORS, RANDOM_STATE


class ModelMetrics(NamedTuple):
        f1: float
        precision: float
        recall: float
        roc_auc: float


class ModelBuilder:

    def __init__(self, X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.Series, y_test: pd.Series):
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

    def build_classifier(self) -> RandomForestClassifier:
        classifier = RandomForestClassifier(n_estimators=N_ESTIMATORS, criterion=CRITERION, random_state=RANDOM_STATE)
        classifier.fit(self.X_train, self.y_train)
        return classifier

    def prediction(self, classifier) -> np.ndarray:
        y_pred = classifier.predict(self.X_test)
        return y_pred

    def get_metrics(self, y_pred) -> OrderedDict:
        return ModelMetrics(f1=f1_score(self.y_test, y_pred),
                            precision=precision_score(self.y_test, y_pred),
                            recall=recall_score(self.y_test, y_pred),
                            roc_auc=roc_auc_score(self.y_test, y_pred))._asdict()
