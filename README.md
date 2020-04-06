# Run web app with fine-tuned GPT-2 model
Setup virtual environment (optional) and install requirements:
``` 
virtualenv --system-site-packages -p python3 venv
source env/bin/activate
venv/bin/pip3 install -r requirements.txt
```

Download [this folder](https://drive.google.com/open?id=12SJMB-dT5Cp-psRH2n9CsbzDS85L1GzD) and copy to `webapp/gpt2/models/355M`:

Run the web application: 
```
python webapp/app.py
```
# Fine-tune GPT-2 from the beginning

# UKP model
Slight modification:
- Save_and_load.py: only for loading trained model (for further training)

    command: `python3 Save_and_Load.py [model_name]`
    
- RunModel_CoNLL_Format.py: add third parameter to specify the directory of the output file

    command: `python3 RunModel_CoNLL_Format.py [model_name] [conll_file] [stored_location]`

# Rhyme extractor

Import the rhyme class:
```
from rhyme.rhyme import Rhyme
```

Create an instance of Rhyme and load the associated model:
```
r = Rhyme()
r.load_model()
```

Predict if a pair of words rhymes or not:
```
r.predict_words(<word1>, <word2>)
```

Example:
```
r.predict_words('fly', 'high')
>>> 1.0
```

Predict a rhyme sequence from a list of words:
```
r.predict_seq(<list of words>)
```

Example:
```
s = ['fly', 'high', 'sleep', 'keep']
r.predict_seq(s)
>>> 'aabb'
```

In case there is a ModuleNotFound error:
```
r.fix_vocab()
```
should fix it

# Time epoch extractor

Download the trained model from [here](https://drive.google.com/file/d/1qavgcVHfoJ0f3hHUn8Q5nPMDs2J5AfoF/view?usp=sharing) and unzip it in model/

Import the epoch class:
```
from epoch.epoch import Epoch
```

Return values
```
  - [1,0,0,0]: 1500-1700
  - [0,1,0,0]: 1700-1800
  - [0,0,1,0]: 1800-1850
  - [0,0,0,1]: 1850-2000
```

Create an instance of the class and predict a stanza with it:
```
text = ["From the day that I first knew you,",
        "Your heart was pure and kind;",
        "Your smile was sweet and innocent,",
        "Your wit was well refined."]

e = Epoch()
e.predict(text)
>>> [0,0,0,1]
```

# Training codes
Training codes for the respective models are also provided:

- Rhyme:

The model is trained entirely using the code [here](https://github.com/dhwajraj/deep-siamese-text-similarity) with the data extracted from given datasets
The code to extract the data can be found:
```
cd training/rhyme
python rhyme_pair_finder.py
```

- Epoch:
Make sure simpletransformers is installed (if requirements.txt is executed before then it should've already been installed):
```
pip install simpletransformers
```

Training with roberta-base, 5 epochs on english poems only

```
cd training/epoch
python train_epoch.py
```

- Stanza-level sentiment classifier:

Make sure simpletransformers is installed (if requirements.txt is executed before then it should've already been installed):
```
pip install simpletransformers
```

Training with bert-base-multilingual-cased, 15 epochs on both english and german poems

```
cd training/sent/stanza_level
python train_sent.py
```

