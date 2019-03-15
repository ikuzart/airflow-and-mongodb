from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from typing import Dict

from data import DataContainer, FeatureStats

import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split


class DataLoader(metaclass=ABCMeta):

    @abstractmethod
    def load_data(self)-> pd.DataFrame:
        pass


class DataToPreprocess(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader

    @abstractmethod
    def get_stats_from_data(self) -> Dict[str, OrderedDict]:
        pass


class Preprocessor(metaclass=ABCMeta):

    def __init__(self, data_to_preprocess: DataToPreprocess):
        self.data_to_preprocess = data_to_preprocess

    @abstractmethod
    def preprocess(self, **kwargs) -> DataContainer:
        pass


class BreastCancerDataLoader(DataLoader):

    def __init__(self):
        self.data = load_breast_cancer()
        self.feature_names = list(self.data['feature_names'])

    def load_data(self) -> pd.DataFrame:
        df = pd.DataFrame(data=np.c_[self.data['data'], self.data['target']],
                          columns=self.feature_names + ['target'])
        return df


class BreastCancerData(DataToPreprocess):

    def __init__(self, data_loader: DataLoader):
        super().__init__(data_loader)
        self.df = self.data_loader.load_data()
        self.df_described = self.df.describe()
        self.df_corr = self.df.corr()
        self.s_quantile = self.df.quantile()

    def _get_feature_stats(self, series: pd.Series) -> FeatureStats:
        return FeatureStats(dtype=str(series.dtype),
                            count=self.df_described[series.name].loc['count'],
                            mean=self.df_described[series.name].loc['mean'],
                            std=self.df_described[series.name].loc['std'],
                            min=self.df_described[series.name].loc['min'],
                            percentile_25=self.df_described[series.name].loc['25%'],
                            percentile_50=self.df_described[series.name].loc['50%'],
                            percentile_75=self.df_described[series.name].loc['75%'],
                            max=self.df_described[series.name].loc['max'],
                            nan=self.df_described[series.name].loc['count'],
                            corr=self.df_corr[series.name].to_dict(),
                            corr_to_target=self.df_corr[series.name].loc['target'],
                            quantile=self.s_quantile.loc[series.name]
                            )

    def get_stats_from_data(self) -> Dict[str, OrderedDict]:
        stats_from_data = {}
        for column in self.df.columns:
            stats_from_data[column] = self._get_feature_stats(self.df[column])._asdict()

        return stats_from_data


class BreastCancerDataPreprocessor(Preprocessor):

    def __init__(self, data_to_preprocess: DataToPreprocess, data_container: DataContainer):
        super().__init__(data_to_preprocess)
        self.df = self.data_to_preprocess.df
        self.data = data_container
        self.data.features_stats = self.data_to_preprocess.get_stats_from_data()
        self.feature_names = self.data_to_preprocess.data_loader.feature_names

    def _split(self, test_size, random_state):
        self.data.X_train, self.data.X_test, self.data.y_train, self.data.y_test = \
            train_test_split(self.df[self.feature_names],
                             self.df['target'],
                             test_size=test_size,
                             random_state=random_state)
        self.data.test_size = test_size
        self.data.random_state = random_state

    def preprocess(self, test_size, random_state) -> DataContainer:
        self._split(test_size, random_state)
        return self.data
