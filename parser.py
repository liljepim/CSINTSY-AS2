import argparse

import pandas as pd


def parse_tsv(tsv_file, text_file):
    df = pd.read_csv(tsv_file, sep="\t", header=None, usecols=[2])
    with open(text_file, "w") as f:
        for line in df[2].tolist():
            f.write(f"{line}\n")
    print(f"Corpora text file created as {text_file}.txt.")


def main(tsv_file, text_file):
    parse_tsv(tsv_file, text_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="parser.py",
        description="Parses sentences from a Tab Separated Value (TSV) file downloaded from Tatoeba",
    )

    try:
        parser.add_argument(
            "-t",
            "--tsv",
            help="Specifies the filename of the TSV file to parse (example: tg_sentences.tsv)",
        )
        parser.add_argument(
            "-o",
            "--output",
            help="Specifies the filename for the output text file (example: tagalo.txt)",
        )
        args = parser.parse_args()

        main(args.tsv, args.output)
    except Exception as e:
        print(e)
        parser.print_help()
