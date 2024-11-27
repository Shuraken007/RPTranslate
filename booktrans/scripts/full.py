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
from ..file_converter import convert_txt_to_epub, convert_txt_to_docx, convert_docx_to_txt

@yadopt.wrap(__doc__)
def main(args: yadopt.YadOptArgs):
   s = Script(args.book_name)
   #yandex
   # concat(s)
   # clear(s)
   # replace_before(s)
   # convert_txt_to_docx(s)
   # convert_docx_to_txt(s)
   # convert_txt_to_epub(s)


   ##google   
   concat(s)
   clear(s)
   replace_before(s)
   # translate(s)
   # replace_after(s)
   # convert_txt_to_epub(s)

if __name__ == '__main__':
   main()