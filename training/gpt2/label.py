import argparse
import os
import sys

path = os.path.abspath(os.path.join(__file__, "../../.."))
sys.path.insert(1, path)

from rhyme.rhyme import RhymeExtractor
from sentiment.sentiment import SentimentExtractor
from utils.reader import Reader

parser = argparse.ArgumentParser(description='Label the txt file')

parser.add_argument('input',
                    metavar='txt_file',
                    type=str,
                    help='The path to txt file')

args = parser.parse_args()

model_rhyme = RhymeExtractor()
sent = SentimentExtractor()
model_rhyme.load_model()
counter = 1

src = args.input
dest = src.replace("_txt", "_labeled")
reader = Reader(src)

# Read src file line by line
with open(src, mode="r", encoding="utf-8") as src_file:
    content = src_file.readlines()
# Open dest file
dest_file = open(dest, mode="a", encoding="utf-8")
stanza = list()
header = ""
footer = ""
time_epoch = ""
sentiment = ""
tracker = 0

# Define time epoch based on name of txt file
if ("1600" in src and "1700" in src) or ("1500" in src and "1600" in src):
    time_epoch = "0"
elif "1700" in src and "1800" in src:
    time_epoch = "1"
elif "1800" in src and "1850" in src:
    time_epoch = "2"
elif ("1850" in src and "1875" in src) or ("1875" in src and "1900" in src) or "2000" in src:
    time_epoch = "3"

# Write file
for line in content:
    is_footer = False
    if ("<|startoftext|>" in line):
        header = line
        stanza = list()
        continue
    if ("<|endoftext|>" in line):
        footer = line
        is_footer = True
    if not is_footer:
        stanza.append(line)
    else:
        rhyme = model_rhyme.predict_seq(reader.get_ending_words(stanza))
        sentiment = sent.sentiment_label(
            sent.sentiment_score(sent.count_sentiment(sent.list_2_str(stanza))[0],
                                 sent.count_sentiment(sent.list_2_str(stanza))[1]))
        header = header.replace("SENTIMENT_LABEL", sentiment)
        header = header.replace("RHYME_SCHEME", rhyme)
        header = header.replace("TIME_EPOCH", time_epoch)

        dest_file.write(header)
        tracker += 1
        print(tracker)
        for line in stanza:
            dest_file.write(line)
            tracker += 1
            print(tracker)
        dest_file.write(footer)
        tracker += 1
        print(tracker)

src_file.close()
dest_file.close()

counter += 1
