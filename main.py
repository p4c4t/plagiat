import argparse
import models

parser = argparse.ArgumentParser()
parser.add_argument("input_file", type=str)
parser.add_argument("output_file", type=str)
args = parser.parse_args()
input_file, output_file = args.input_file, args.output_file
with open(input_file) as inp:
    with open(output_file, "w") as out:
        for line in inp:
            file1, file2 = line.split(' ')
            score = models.score(file1, file2)
            out.write(f"{score}\n")
