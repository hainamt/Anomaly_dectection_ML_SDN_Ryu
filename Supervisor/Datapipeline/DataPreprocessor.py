import joblib
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn import preprocessing as pp
from features import rm_attrs, attrs


class AttributesRemover(BaseEstimator, TransformerMixin):
    def __init__(self, rm_columns = rm_attrs):
        self.rm_columns = rm_columns
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        return X.drop(columns=self.rm_columns, axis=1)

class CustomCleaner(TransformerMixin):
    def __init__(self, *args, **kwargs):
        pass
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        return X[~X.isin([np.nan, np.inf, -np.inf]).any(1)]

class Standardizer(TransformerMixin):
    def __init__(self, columns=attrs):
        self.stdizer = pp.MinMaxScaler()
        self.columns = columns
    def fit(self, X, y):
        self.stdizer.fit(X)
        return self
    def transform(self, X, y=None):
        return self.stdizer.transform(X)

class PipelineLoader(object):
    def __init__(self, pipeline_filename):
        self.ids_pipeline = joblib.load(pipeline_filename)
    def getPipeline(self):
        return self.ids_pipeline
