import spacy
import os
import sys

path = os.path.abspath(os.path.join(__file__, "../../.."))
sys.path.insert(1, path)


class SentimentExtractor:
    nlp = spacy.load("en_core_web_sm")

    positive = []
    with open('model/sentiment/opinion-lexicon-english/positive-words.txt', 'r', encoding='ISO-8859-1') as f:
        lines = f.readlines()
    for line in lines:
        if ';' in line or line == '\n':
            continue
        positive.append(line.strip('\n'))

    negative = []
    with open('model/sentiment/opinion-lexicon-english/negative-words.txt', 'r', encoding='ISO-8859-1') as f:
        lines = f.readlines()
    for line in lines:
        if ';' in line or line == '\n':
            continue
        negative.append(line.strip('\n'))

    def count_sentiment(self, s):
        pos_count = 0
        neg_count = 0
        docs = self.nlp(s)
        for token in docs:
            if token.lemma_ in self.positive:
                pos_count = pos_count + 1
            if token.lemma_ in self.negative:
                neg_count = neg_count + 1
        return pos_count, neg_count

    def list_2_str(self, poem):
        return ' '.join(poem)

    def sentiment_score(self, pos, neg):
        if pos + neg == 0:
            return 0
        return (pos - neg) / (pos + neg)

    def sentiment_label(self, score):
        if score > 0:
            return 'positive'
        elif score < 0:
            return 'negative'
        else:
            return 'neutral'


"""
	poem = ["From the day that I first knew you,",
        "Your heart was pure and kind;",
        "Your smile was sweet and innocent,",
        "Your wit was well refined."]

	sentence = list_2_str(poem)
	p,n = count_sentiment(sentence)
	sentiment_label(sentiment_score(p,n))
"""
