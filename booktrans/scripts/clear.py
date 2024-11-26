"""
Usage:
   cmd <book_name>
   cmd --help

Remove specific blocks from book, using config.py in book folder

Arguments:
   book_name     searching for book in input folder

Other options:
    -h, --help      Show this help message and exit.
"""

import yadopt
from ..script import Script
from ..clear import clear

@yadopt.wrap(__doc__)
def main(args: yadopt.YadOptArgs):
   s = Script(args.book_name)
   clear(s)

if __name__ == '__main__':
   main()