# Copyright (C) 2025 by Higher Expectations for Racine County

from argparse import ArgumentParser

# from functools import reduce

parser = ArgumentParser(
    prog="smelt_py",
    description="Work with data about Early Literacy downloaded from Panorama"
)

parser.add_argument("-o", "--output",
                    help="the output file",
                    required=True)
parser.add_argument("input_files",
                    nargs="+",
                    action="extend")

args = parser.parse_args()

print(args.output)
print(args.input_files)

# file_fields = [read_headers(f) for f in args.input_files]

# totes = reduce(lambda lhs, rhs: lhs.vstack(rhs), file_fields)

# totes.write_csv(args.output)
