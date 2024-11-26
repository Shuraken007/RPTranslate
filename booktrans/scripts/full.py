"""
Usage:
   cmd <book_name>
   cmd --help

Run all cycle for book, if config existed.

Arguments:
   book_name     searching for book in input folder

Other options:
    -h, --help      Show this help message and exit.
"""

import yadopt
from ..script import Script
from ..clear import clear
from ..translate import translate
from ..concat import concat
from ..replace import replace_before, replace_after

@yadopt.wrap(__doc__)
def main(args: yadopt.YadOptArgs):
   s = Script(args.book_name)
   concat(s)
   clear(s)
   replace_before(s)
   translate(s)
   replace_after(s)

if __name__ == '__main__':
   main()