from collections import OrderedDict
from typing import Dict, NamedTuple


class FeatureStats(NamedTuple):
    dtype: str
    count: float
    mean: float
    std: float
    min: float
    percentile_25: float
    percentile_50: float
    percentile_75: float
    max: float
    nan: float
    corr: Dict[str, float]
    corr_to_target: float
    quantile: float
    # distplot: bytes
    # pairplot: bytes


class DataContainer:
    features_stats: Dict[str, OrderedDict] = {}
    X_train = None
    X_test = None
    y_train = None
    y_test = None
    test_size = None
    random_state = None
