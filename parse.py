from lib import Nem12Parser

import argparse

cli = argparse.ArgumentParser(
    prog="NEM12 Parser",
    description="Extracts meter readings from NEM12 files and generates corresponding SQL insert statements",
)

cli.add_argument("file", type=argparse.FileType("r"))
args = cli.parse_args()


for reading in Nem12Parser(args.file):
    print(reading.to_sql())
