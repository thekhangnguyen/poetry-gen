import xml.etree.ElementTree as ET
import re
import os
import sys

path = os.path.abspath(os.path.join(__file__, "../../.."))
sys.path.insert(1, path)


class Reader:
    def __init__(self, path):
        self.path = path
        self.poem = list()

    # Read from xml and create list of stanzas in a poem (1 xml = 1 poem)
    def get_poem(self):
        root = ET.parse(self.path).getroot()
        self.poem = list()

        for lg in root.iter('{http://www.tei-c.org/ns/1.0}lg'):
            # Look for stanza
            if (lg.get('type') == 'stanza'):
                stanza = list()
                prev_stanza = list()
                sroot = lg
                # Read every line
                for l in sroot.iter('{http://www.tei-c.org/ns/1.0}l'):
                    # Ignore empty lines and lines with only special characters or numbers
                    if (l.text != "" and re.search('[a-zA-Z]', str(l.text))):
                        line = str(l.text)
                        # Strip off leading or trailing spaces
                        line = line.strip()
                        # Remove redundant spaces in between
                        line = line.replace(" ,", ",")
                        line = line.replace(" ?", "?")
                        line = line.replace(" .", ".")
                        line = line.replace(" !", "!")
                        line = line.replace(" :", ":")
                        line = line.replace(" ;", ";")
                        line = line.replace(" -", "-")
                        line = line.replace(" '", "'")
                        line = line.replace("' ", "'")
                        line = line.replace("\u2018 ", "\u2018").replace("\x91 ", "\x91")
                        line = line.replace(" \u2019", "\u2019").replace(" \x92", "\x92")
                        line = line.replace("\u201C ", "\u201C").replace("\x93 ", "\x93")
                        line = line.replace(" \u201D", "\u201D").replace(" \x94", "\x94")

                        line = line.replace(" [= e ]", "e")
                        line = line.replace(" [= o ]", "o")
                        line = line.replace(" [= a ]", "a")
                        line = line.replace(" [= u ]", "u")
                        line = line.replace(" [= i ]", "i")
                        line = line.replace("=", "")
                        line = line.replace("\u2019 d", "\u2019d")
                        line = line.replace("\x92 d", "\x92d")
                        line = re.sub("\{ [0-9]+ \}", "", line)
                        line = re.sub("\[ [0-9]+ \]", "", line)
                        line = re.sub("\( [0-9]+ \)", "", line)
                        line = re.sub("\{ [a-zA-Z] \}", "", line)
                        line = re.sub("\[ [a-zA-Z] \]", "", line)
                        line = re.sub("\( [a-zA-Z] \)", "", line)
                        line = re.sub("\{ [a-zA-Z][a-zA-Z] \}", "", line)
                        line = re.sub("\[ [a-zA-Z][a-zA-Z] \]", "", line)
                        line = re.sub("\( [a-zA-Z][a-zA-Z] \)", "", line)
                        line = line.replace(" n't", "n't")
                        line = line.replace(" n\x92t", "n\x92t")
                        line = line.replace(" n\u2019t", "n\u2019t")
                        line = line.replace(" 's ", "'s ")
                        line = line.replace(" 'm ", "'m ")
                        line = line.replace(" 've ", "'ve ")
                        line = line.replace(" \u2018s ", "\u2018s ")
                        line = line.replace(" \u2018m ", "\u2018m ")
                        line = line.replace(" \u2018ve ", "\u2018ve ")
                        line = line.replace(" \x91s ", "\x91s ")
                        line = line.replace(" \x91m ", "\x91m ")
                        line = line.replace(" \x91ve ", "\x91ve ")
                        line = line.replace("( ", "").replace(" )", "")
                        line = line.replace("{ ", "").replace(" }", "")
                        line = line.replace("[ ", "").replace(" ]", "")
                        line = line.replace("(", "").replace(")", "")
                        line = line.replace("{", "").replace("}", "")
                        line = line.replace("[", "").replace("]", "")
                        line = re.sub(" +", " ", line)
                        line = line.strip()
                        if len(line) > 0:
                            c = line[-1]
                            while not (
                                    c.isalpha() or c == "?" or c == "!" or c == "\u2019" or c == "\x92" or c == "\u201D" or c == "\x94"):
                                line = line[:-1]
                                c = line[-1]
                            line = line.strip()
                        else:
                            continue

                        stanza.append(line)

                if (len(stanza) > 3 and len(stanza) < 11):
                    self.poem.append(stanza)
                    stanza = list()

                ''' 4-line stanza              
                    # Save every 4 lines
                    if (len(stanza) == 4):
                      self.poem.append(stanza)
                      prev_stanza = stanza
                      stanza = list()
        
                
                # Redundant lines are complemented by lines from previous stanza
                if (len(prev_stanza) != 0):
                  if (len(stanza) == 1):
                    stanza.insert(0, prev_stanza[3])
                    stanza.insert(0, prev_stanza[2])
                    stanza.insert(0, prev_stanza[1])
                    self.poem.append(stanza)
                  elif (len(stanza) == 2):
                    stanza.insert(0, prev_stanza[3])
                    stanza.insert(0, prev_stanza[2])
                    self.poem.append(stanza)
                  elif (len(stanza) == 3):
                    stanza.insert(0, prev_stanza[3])
                    self.poem.append(stanza)
                '''
        return self.poem

    # Get list of lowered ending words
    def get_ending_words(self, stanza):
        ending_words = list()
        for line in stanza:
            # Get the ending word
            while ((not line[-1].isalpha()) and len(line) > 1):
                line = line[:-1]
            line = line.strip()
            word = line.split(" ")[-1].split("\n")[0]
            ending_words.append(word.lower())

        return ending_words

    # Convert poems to txt with format:
    # <|startoftext|> [RHYME_SCHEME, SENTIMENT_LABEL, TIME_EPOCH]
    # ...
    # <|endoftext|>
    def convert_to_txt(self, src, dest):
        file = open(dest, mode="a", encoding="utf-8")
        for stanza in self.poem:
            file.write("<|startoftext|> " + "[RHYME_SCHEME, SENTIMENT_LABEL, TIME_EPOCH]\r\n")
            for line in stanza:
                file.write(line + "\r\n")
            file.write("<|endoftext|>\r\n")
        file.close()
