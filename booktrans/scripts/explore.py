"""
Usage:
   cmd <book_name>
   cmd --help

Explore usefull data from text. Proper nouns.

Arguments:
   book_name     searching for book in input folder

Other options:
    -h, --help      Show this help message and exit.
"""

import yadopt
from ..script import Script
from ..explore import explore

@yadopt.wrap(__doc__)
def main(args: yadopt.YadOptArgs):
   s = Script(args.book_name)
   explore(s)

if __name__ == '__main__':
   main()