import tensorflow as tf
import sys
import os
import numpy as np
import pickle

path = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.insert(1, path)
path = os.path.abspath(os.path.join(__file__, ".."))
sys.path.insert(1, path)

from input_helpers import InputHelper

vocab_filepath = "model/rhyme/vocab"
meta_filepath = "model/rhyme/model-11000.meta"
ckpt_filepath = "model/rhyme/model-11000"


class Rhyme:
    def __init__(self):
        self.session = tf.Session()

    def load_model(self):
        saver = tf.train.import_meta_graph(meta_filepath)
        saver.restore(self.session, ckpt_filepath)

    def fix_vocab(self):
        # Fix the vocab file if there is an error called
        # 'copy_reg/r' not found
        a = open(vocab_filepath, 'r').readlines()
        a = map(lambda x: x.replace("\r\n", "\n"), a)

        with open(vocab_filepath, 'w') as f:
            for i in a:
                f.write(i)

    def predict_words(self, word1, word2):
        inpH = InputHelper()

        w1, w2, dim = inpH.getWords(word1, word2, vocab_filepath, 30)
        graph = tf.get_default_graph()

        with graph.as_default():
            input_x1 = graph.get_operation_by_name("input_x1").outputs[0]
            input_x2 = graph.get_operation_by_name("input_x2").outputs[0]

            dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]
            sim = graph.get_operation_by_name("accuracy/temp_sim").outputs[0]

            r1 = self.session.run([sim], {input_x1: w1, input_x2: w2, dropout_keep_prob: 1.0})
            r2 = self.session.run([sim], {input_x1: w2, input_x2: w1, dropout_keep_prob: 1.0})

            r = max(r1, r2)

        return r[0][0]

    def predict_seq(self, seq):
        rhyme_scheme = {}
        letters = ['a', 'b', 'c', 'd']
        for i, word in enumerate(seq):
            if word in rhyme_scheme.keys():
                continue
            rhyme_scheme[word] = 0
            found_rhyme = False
            for j in range(i):
                p_word = seq[j]
                if self.predict_words(p_word, word) == 1:
                    found_rhyme = True
                    if rhyme_scheme[p_word] == 0:
                        num = 1
                        while num in rhyme_scheme.values():
                            num += 1
                        rhyme_scheme[p_word] = letters[num - 1]
                        letters.pop(num - 1)
                    rhyme_scheme[word] = rhyme_scheme[p_word]
        for key in rhyme_scheme:
            if rhyme_scheme[key] == 0:
                rhyme_scheme[key] = letters[0]
                letters.pop(0)
        scheme = ''
        for s in seq:
            scheme += rhyme_scheme[s]
        return scheme

    def close_session(self):
        os.chdir(os.path.dirname(dname))
        self.session.close()
