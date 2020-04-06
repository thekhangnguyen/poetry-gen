import argparse
import os
import sys

path = os.path.abspath(os.path.join(__file__, "../../.."))
sys.path.insert(1, path)

parser = argparse.ArgumentParser(description='Join the labeled txt files')

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
        dest = path + ".txt"
        # Debug
        print("File %d at: %s" % (counter, src))

        src_file = open(src, 'r', encoding='utf8')
        dest_file = open(dest, 'a', encoding='utf8')

        lines = src_file.readlines()
        for line in lines:
            dest_file.write(line)

        src_file.close()
dest_file.close()

counter += 1
