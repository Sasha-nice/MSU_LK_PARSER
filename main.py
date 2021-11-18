import sys
import contextlib
from scrapper import MsuParser

if __name__ == '__main__':
    with contextlib.redirect_stderr(None):
        parser = MsuParser(sys.argv[1], sys.argv[2])
        parser.start()
