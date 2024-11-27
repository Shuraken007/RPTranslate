"""
Usage:
   cmd <book_name>
   cmd --help

Convert file to epub

Arguments:
   book_name     searching for book in input folder

Other options:
    -h, --help      Show this help message and exit.
"""

import yadopt

from ..script import Script
from ..file_converter import convert_txt_to_epub

@yadopt.wrap(__doc__)
def main(args: yadopt.YadOptArgs):
   s = Script(args.book_name)
   convert_txt_to_epub(s)

if __name__ == '__main__':
   main()   