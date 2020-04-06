# This script trains the BiLSTM-CRF architecture for part-of-speech tagging
# and stores it to disk. Then, it loads the model to continue the training.
# For more details, see docs/Save_Load_Models.md
from __future__ import print_function
import os
import logging
import sys
from neuralnets.BiLSTM import BiLSTM
from util.preprocessing import perpareDataset, loadDatasetPickle



# :: Change into the working dir of the script ::
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# :: Logging level ::
loggingLevel = logging.INFO
logger = logging.getLogger()
logger.setLevel(loggingLevel)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(loggingLevel)
formatter = logging.Formatter('%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


######################################################
#
# Data preprocessing
#
######################################################
datasets = {
  'sentiment2':
        {'columns': {0:'tokens', 1:'sent_1_BIO'},
         'label': 'sent_1_BIO',
         'evaluate': True,
         'commentSymbol': None}
} 


# :: Path on your computer to the word embeddings. Embeddings by Komninos et al. will be downloaded automatically ::
embeddingsPath = 'more_embedding.tsv'

# :: Prepares the dataset to be used with the LSTM-network. Creates and stores cPickle files in the pkl/ folder ::
pickleFile = perpareDataset(embeddingsPath, datasets)


######################################################
#
# The training of the network starts here
#
######################################################

modelPath = sys.argv[1]

#Load the embeddings and the dataset
embeddings, mappings, data = loadDatasetPickle(pickleFile)
# Some network hyperparameters

print("\n\n\n\n------------------------")
print("Load the model and continue training")
newModel = BiLSTM.loadModel(modelPath)
print('load model ' + modelPath)
newModel.setDataset(datasets, data)
newModel.params['earlyStopping'] = 25
newModel.modelSavePath = "models/[ModelName]_[DevScore]_[TestScore]_[Epoch].h5"
newModel.fit(epochs=70)

print("retrained model store at "+newModel.modelSavePath)

