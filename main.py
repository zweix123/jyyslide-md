import argparse
from src.converter import converter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="select a Markdown file to convert", type=str)
    args = parser.parse_args()

    converter(args.filepath)
