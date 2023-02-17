import sys
import lib

if __name__ == "__main__":
    for tar_file in sys.argv[1:]:
        lib.process(tar_file)
    pass