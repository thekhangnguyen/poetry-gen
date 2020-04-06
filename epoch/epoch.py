import sys
import os

path = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.insert(1, path)
path = os.path.abspath(os.path.join(__file__, ".."))
sys.path.insert(1, path)

from simpletransformers.classification import MultiLabelClassificationModel

"""
Return values
  - [1,0,0,0]: 1500-1700
  - [0,1,0,0]: 1700-1800
  - [0,0,1,0]: 1800-1850
  - [0,0,0,1]: 1850-2000

"""


class Epoch:
    def __init__(self):
        self.model_type = 'roberta'
        self.path = 'model/epoch'
        self.num_labels = 4
        self.args = {"reprocess_input_data": True, "overwrite_output_dir": True, "num_train_epochs": 1, 'fp16': False}
        self.model = MultiLabelClassificationModel(model_type=self.model_type, model_name=self.path,
                                                   num_labels=self.num_labels, args=self.args)

    def preprocess(self, text):
        result = ''
        for line in text:
            result = result + ' </br> ' + line
        return result[7:]

    def predict(self, text):
        predictions, values = self.model.predict([self.preprocess(text)])
        return predictions[0]
