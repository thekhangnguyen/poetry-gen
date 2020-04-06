import argparse
import os
import sys

path = os.path.abspath(os.path.join(__file__, "../../.."))
sys.path.insert(1, path)
from utils.reader import Reader

parser = argparse.ArgumentParser(description='Convert xml to txt')

parser.add_argument('input',
                    metavar='input_folder',
                    type=str,
                    help='The path to input folder')

args = parser.parse_args()

path = args.input

counter = 1

for (dirpath, dirnames, filenames) in os.walk(path):
    for filename in filenames:
        src = os.path.join(dirpath, filename)

        # Debug
        print("File %d at: %s" % (counter, src))

        dest = dirpath + "_txt.txt"

        try:
            reader = Reader(src)
            reader.get_poem()
            reader.convert_to_txt(src, dest)
        except:
            print("Error: Skip this file")
            continue

        counter += 1
