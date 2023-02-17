import sys
from src.converter import converter

if __name__ == "__main__":
    for tar_file in sys.argv[1:]:
        converter(tar_file)
