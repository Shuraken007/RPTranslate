"""
Usage:
   cmd <book_name>
   cmd --help

Replace proper nouns from config

Arguments:
   book_name     searching for book in input folder

Other options:
    -h, --help      Show this help message and exit.
"""

import yadopt
from ..script import Script
from ..replace import replace_before

@yadopt.wrap(__doc__)
def main(args: yadopt.YadOptArgs):
   s = Script(args.book_name)
   replace_before(s)

if __name__ == '__main__':
   main()