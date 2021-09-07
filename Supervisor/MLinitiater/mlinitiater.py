import joblib
import requests
from Datapipeline.DataPreprocessor import PipelineLoader

class MLInitiater(object):
    def __init__(self, model_file, data_pipeline_file):
        self.model=joblib.load(model_file)
        self.ppl = PipelineLoader(data_pipeline_file).getPipeline()

    def predict(self, data):
        preprocess_data = self.ppl.transform(data)
        return self.model.predict(preprocess_data)

