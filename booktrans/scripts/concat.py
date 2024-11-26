"""
Usage:
   cmd <book_name>
   cmd --help

Concatenate book txt files into one.

Arguments:
   book_name     searching for book in input folder

Other options:
    -h, --help      Show this help message and exit.
"""

import yadopt
from ..script import Script
from ..concat import concat

@yadopt.wrap(__doc__)
def main(args: yadopt.YadOptArgs):
   s = Script(args.book_name)
   concat(s)

if __name__ == '__main__':
   main()