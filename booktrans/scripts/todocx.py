"""
Usage:
   cmd <book_name>
   cmd --help

Convert file to docx

Arguments:
   book_name     searching for book in input folder

Other options:
    -h, --help      Show this help message and exit.
"""

import yadopt
from ..script import Script
from ..const import REPLACE_BEFORE
from docx import Document
from pathlib import Path

def get_document(path):
   document = Document()
   filedata = open(path).read()
   document.add_paragraph(filedata)

   docx_path = Path(path).with_suffix('.docx')
   print(docx_path)
   document.save(docx_path)

@yadopt.wrap(__doc__)
def main(args: yadopt.YadOptArgs):
   s = Script(args.book_name)
   file = s.get_out_file(REPLACE_BEFORE)
   get_document(file)

if __name__ == '__main__':
   main()