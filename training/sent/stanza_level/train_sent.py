import sys
import os

from simpletransformers.classification import MultiLabelClassificationModel

import csv
import pandas as pd
import xml.etree.ElementTree as ET

from random import shuffle
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import multilabel_confusion_matrix
from string import punctuation

root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
fgrab_path = os.path.join(root_path, 'utils')
sys.path.append(fgrab_path)

from grab_folder import fgrab

def get_stanza_w_info(stanza):
  text = [line[0].strip().translate(str.maketrans('', '', punctuation)) for line in stanza]

  lines = ''
  for line in text:
    lines = lines + ' </br> ' + line
  lines = lines[7:]

  label_1 = []
  label_2 = []

  label_1 = [line[1].split('---') for line in stanza]
  label_1 = [item.strip().lower() for sublist in label_1 for item in sublist]

  label_2 = [line[2].split('---') for line in stanza if len(line) > 2]
  label_2 = [item.strip().lower() for sublist in label_2 for item in sublist]

  labels = list(set(label_1 + label_2))
  if 'nostalgia' in labels:
    labels.remove('nostalgia')

  labels = [label.replace(' ', '') for label in labels]

  return lines, labels

labels = ['suspense', 'awe/sublime', 'sadness', 'annoyance', 'uneasiness', 'beauty/joy', 'vitality', 'humor']

def assign_label(t):
  vector = [0, 0, 0, 0, 0, 0 ,0 ,0]
  for l in t[1]:
    index = labels.index(l)
    vector[index] = 1
  
  return [t[0], vector]

def get_label_count(data):
  vector = [0, 0, 0, 0, 0, 0 ,0 ,0]
  for stanza in data:
    for i in range(8):
      vector[i] = vector[i] + stanza[1][i]
  return vector

def get_data_from_xml_poem(xml_file):
  root = ET.parse(xml_file).getroot()
  data = []
  for lg in root.iter('{http://www.tei-c.org/ns/1.0}lg'):
    if 'type' in lg.attrib and lg.attrib['type'] == 'poem':
      for slg in lg:
        if 'type' in slg.attrib and slg.attrib['type'] == 'stanza':
          stanza = []
          for l in slg:
            np = " "
            if l.text == None:
              continue
            text = l.text
            if text.split()[-1].isdigit():  # Clean the line count at the end of some lines
              text = text.rsplit(' ', 1)[0]
            for t in text:  # Clean punctuation
              if t not in punctuation:
                np = np + t
            if 'emo2' in l.attrib and l.attrib['emo2'] != None:
              stanza.append([" ".join(np.split()), l.attrib['emo1'], l.attrib['emo2']])
            else:
              stanza.append([" ".join(np.split()),l.attrib['emo1']])
          data.append(stanza)
    return data

data_0 = []
folder = fgrab(os.path.join(root_path, 'dataset/german/poetry-emotion-master/XMLGold')).get_all_in_dir('.xml')
for f in folder:
  data_0.extend(get_data_from_xml_poem(f))
  
data_0 = [assign_label(get_stanza_w_info(s)) for s in data_0]

data_1 = []
data_2 = []

array = [data_1, data_2]

files = [os.path.join(root_path, 'dataset/german/german.tsv'),
         os.path.join(root_path, 'dataset/english/english.tsv')]

for j in range(2):
  count = 0
  with open(files[j]) as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    raw = [row for row in reader]

    stanza = []
    for i in range(len(raw)):
      if len(raw[i]) > 1 and raw[i][1] == '':
        count = count + 1
      if len(raw[i]) > 1 and raw[i][1] != '':
        stanza.append(raw[i])
      if raw[i] == []:
        array[j].append(stanza)
        stanza = []

data_1 = [row for row in data_1 if row != []]
data_1 = [assign_label(get_stanza_w_info(s)) for s in data_1]

data_2 = [row for row in data_2 if row != []]
data_2 = [assign_label(get_stanza_w_info(s)) for s in data_2]

de_data = data_0 + data_1
en_data = data_2

shuffle(en_data)

train_data = en_data[:int(0.8*len(en_data))]
test_data = en_data[int(0.8*len(en_data)):]

#train_data = train_data + en_data

shuffle(train_data)

train_df = pd.DataFrame(train_data, columns=["text", "labels"])
eval_df = pd.DataFrame(test_data)

model = MultiLabelClassificationModel(
    "bert",
    "bert-base-multilingual-cased",
    num_labels = 8,
    args={"reprocess_input_data": True, "overwrite_output_dir": True, "num_train_epochs": 15, 'fp16': False},
)

model.train_model(train_df)

sub = test_data

test_label = []
test_text = []
predictions = []

for i in range(len(sub)):
  test_text.append(sub[i][0])
  test_label.append(sub[i][1])

predictions, dummy = model.predict(test_text)
pred = pd.DataFrame(predictions)
pd_label = pd.DataFrame(test_label)

print(f1_score(test_label, predictions, average = None))

print(f1_score(test_label, predictions, average = 'macro'))