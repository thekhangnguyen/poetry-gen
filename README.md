# Introduction
The goal of this project is to create a style-conditioned poetry generator: the user can select desired criteria for the poems (rhyming pattern, sentiment and time epoch). The poetry generator is a GPT-2 model fine-tuned on our labeled dataset (link below) and it can be used by running a web application. 

This project is a students' Bachelor Project (Winter semester 19/20) implemented under the supervision of [Dr. rer. pol. Steffen Eger](https://www.informatik.tu-darmstadt.de/aiphes/aiphes/people_7/mitarbeiter_4_detailseite_72000.en.jsp) at the [Technische Universität Darmstadt](https://www.tu-darmstadt.de/) (Germany).

## Authors of the project
The authors are: The-Khang Nguyen, Thanh Tung Linh Nguyen, Minh Vu Pham and Minh Tung Tran (all are students at the Technische Universität Darmstadt) and the original git repository is  at: https://github.com/thekhangnguyen/poetry-gen

## Implementation of the poetry generator

To label the dataset for fine-tuning the GPT-2 model, we first train 3 extractors for rhyming patterns, sentiment and time epoch, then use the extractors to label the [dataset](https://drive.google.com/open?id=1DiLK0OjE0OwgCgt_bhlChy8DeiZk60JF) from Project Gutenberg. With the labeled dataset, we fine-tune the GPT-2 model until it can generate the desired style-conditioned poetry.

The poetry generator can be assessible by running the web application (instruction below).

## References
The original GPT-2 model (from OpenAI) is available at: https://github.com/openai/gpt-2

# Setup virtual environment (recommended)
Setup virtual environment (optional) and install requirements:
``` 
virtualenv --system-site-packages -p python3 venv
source venv/bin/activate
venv/bin/pip3 install -r requirements.txt
```

# Run web app with fine-tuned GPT-2 model

Download [this zip file](https://drive.google.com/open?id=1dZs3USYTJ7NvEA2rVVfKIG-O23zrPBsg) and extract the content to the folder 355M in `gpt2/models/355M`:

Run the web application: 
```
python webapp/app.py
```
The web application is now assessible via local ip address (remember to free the port 5000 before running the web app)
```
http://127.0.0.1:5000
```
# [Data used to fine-tune GPT-2 model](https://drive.google.com/open?id=1DiLK0OjE0OwgCgt_bhlChy8DeiZk60JF)
To fine-tune the GPT-2 model, we extract all the four-line stanzas from [this dataset](https://github.com/tnhaider/english-gutenberg-poetry), label those stanzas with our extractors (rhyme, sentiment and time epoch) with the format:
><|startoftext|> [RHYME, SENTIMENT, TIME]\
>... (lines of stanza here)\
>...\
>...\
>...\
><|endoftext|>

where RHYME, SENTIMENT and TIME stand for the labels generated by our extractors. E.g. [aabb, positive, 16th]. Then we use the 5-millions-line labeled dataset to fine-tune the GPT-2 model.

# Line-level emotion tagger
This is the training code taken from the [ukp group](https://github.com/UKPLab/emnlp2017-bilstm-cnn-crf) in oder to test if this is a sufficient training method for predicting sentiments in poetries.

The codes are all placed inside the ukp folder. In oder to run any code for the emotion tagger, you need to have ukp as your current working directory.

For further instructions of how to run the codes, you can check the readme file located in the ukp folder [here](https://github.com/thekhangnguyen/poetry-gen/blob/master/ukp/README.md).

Slight modification from the original codes:

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

Download the trained model from [here](https://drive.google.com/file/d/1qavgcVHfoJ0f3hHUn8Q5nPMDs2J5AfoF/view?usp=sharing) and extract its contents into the folder epoch in `model/epoch`

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

# enable_cuda = True if GPU is available, False otherwise

e = Epoch(enable_cuda = <bool>)

e.predict(text)
>>> [0,0,0,1]
```

# Training codes
Training codes for the respective models are also provided:

- Rhyme:

The model is trained entirely using the code [here](https://github.com/dhwajraj/deep-siamese-text-similarity) with the data extracted from given datasets.
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

