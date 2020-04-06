#IMPORTANT: Install this
# pip install simpletransformers

from simpletransformers.classification import MultiLabelClassificationModel

import xml.etree.ElementTree as ET
import sys
import os
import csv
import pandas as pd
import math

root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
fgrab_path = os.path.join(root_path, 'utils')
sys.path.append(fgrab_path)

from grab_folder import fgrab
from string import punctuation
from collections import defaultdict
from random import shuffle
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix

# Data processing. WARNING: Slow

class xreader:
  def __init__(self, path):
    self.path = path
    self.poems = []
    self.br_stanza = []

  def get_poems(self):
    root = ET.parse(self.path).getroot()
    self.poems = list()
    for lg in root.iter('{http://www.tei-c.org/ns/1.0}lg'):
      if 'type' in lg.attrib and lg.attrib['type'] == 'stanza':
        stanza = []
        for l in lg:
          np = " "
          if l.text == None:
            continue
          text = l.text.lower()
          if text.split()[-1].isdigit():  # Clean the line count at the end of some lines
            text = text.rsplit(' ', 1)[0]
          for t in text:  # Clean punctuation
            if t not in punctuation and t not in ['“', '‘', '’']:
              np = np + t
          if len(np) < 20:
            continue
          stanza.append(" ".join(np.split()))
        if len(stanza) > 3 and len(stanza) < 11:
          lines = ''
          for line in stanza:
            lines = lines + ' </br> ' + line
          lines = lines[7:]
          self.br_stanza.append(lines)
          self.poems.append(stanza)
    return self.poems

  def get_lines(self):
    poems = self.get_poems()
    lines = []
    for poem in poems:
      for line in poem:
        lines.append(line)
    return lines

  def get_stanza(self, line_count):
    lines = self.get_lines()
    stanzas = []
    delimiter = math.ceil(len(lines) / line_count)

    for i in range(delimiter):
      s = lines[(i * line_count):(i + 1)*line_count]
      temp = ''
      for i in range(len(s)):
        temp = temp + s[i] + ', '
      temp = temp[:-2] 
      stanzas.append(temp)
    return stanzas
  def get_br_stanza(self):
    self.get_poems()
    return self.br_stanza

def find_duplicates(folder1, folder2):
  f1 = fgrab(folder1).get_all_in_dir('.xml')
  f2 = fgrab(folder2).get_all_in_dir('.xml')
  f1 = [f.split('/')[-1] for f in f1]
  f2 = [f.split('/')[-1] for f in f2]

  dup = set(f1) & set(f2)

  return list(dup)

# Data labeling

folders = [os.path.join(root_path, 'dataset/english/english-gutenberg-poetry-master/1500-1600_Poetry'),
           os.path.join(root_path, 'dataset/english/english-gutenberg-poetry-master/1600-1700_Poetry'),
           os.path.join(root_path, 'dataset/english/english-gutenberg-poetry-master/1700-1800_Poetry'),
           os.path.join(root_path, 'dataset/english/english-gutenberg-poetry-master/1800-1850_Poetry'),
           os.path.join(root_path, 'dataset/english/english-gutenberg-poetry-master/1850-1900_Poetry'),
           os.path.join(root_path, 'dataset/english/english-gutenberg-poetry-master/1900-2000_Poetry')]

print(folders)

poem_16 = []
poem_17 = []
poem_18 = []
poem_19_0 = []
poem_19_1 = []
poem_20 = []

listings = [poem_16, poem_17, poem_18, poem_19_0, poem_19_1, poem_20]

for i in range(6):
  folder = fgrab(folders[i]).get_all_in_dir('.xml')

  for p in folder:
    stanza = xreader(p).get_br_stanza()
    listings[i].extend(stanza)

for l in listings:
  print(len(l))

poem_16_17 = poem_16 + poem_17
poem_19_20 = poem_19_1 + poem_20

raw_data = [poem_16_17, poem_18, poem_19_0, poem_19_20]
labels = [[1,0,0,0],
          [0,1,0,0],
          [0,0,1,0],
          [0,0,0,1]]

labeled_poem_16_17 = []
labeled_poem_18 = []
labeled_poem_19_0 = []
labeled_poem_19_20 = []

labeled_data = [labeled_poem_16_17, labeled_poem_18, labeled_poem_19_0, labeled_poem_19_20]

for i in range(4):
  for r_d in raw_data[i]:
    labeled_data[i].append([r_d, labels[i]])

for l in labeled_data:
  print(len(l))

big_data = labeled_data[0][:15000] + labeled_data[1][10000:40000] + labeled_data[2][30000:60000] + labeled_data[3][:30000]

shuffle(big_data)

train_data = big_data[:int(0.8*len(big_data))]
test_data = big_data[int(0.8*len(big_data)):]

train_df = pd.DataFrame(train_data, columns=["text", "labels"])
eval_df = pd.DataFrame(test_data)

# Load the model
model = MultiLabelClassificationModel(
    "roberta",
    "roberta-base",
    num_labels = 4,
    args={"reprocess_input_data": True, "overwrite_output_dir": True, "num_train_epochs": 5, 'fp16': False},
)

# Train model
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

print(confusion_matrix(pd_label.values.argmax(axis=1), pred.values.argmax(axis = 1)))