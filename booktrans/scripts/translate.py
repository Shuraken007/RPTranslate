"""
Usage:
   cmd <book_name>
   cmd --help

Translate book to language.

Arguments:
   book_name     searching for concat.txt in output/book_name folder

Other options:
    -h, --help      Show this help message and exit.
"""

import yadopt
from ..script import Script
from ..translate import translate

@yadopt.wrap(__doc__)
def main(args: yadopt.YadOptArgs):
   s = Script(args.book_name)
   translate(s)

if __name__ == '__main__':
   main()