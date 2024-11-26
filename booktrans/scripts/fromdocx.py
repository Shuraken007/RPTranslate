"""
Usage:
   cmd <book_name>
   cmd --help

Convert file from docx to txt

Arguments:
   book_name     searching for book in input folder

Other options:
    -h, --help      Show this help message and exit.
"""

import yadopt
from ..script import Script
from ..const import DOCX, TRANSLATE
from docx import Document
from pathlib import Path

def get_document(script, path):
   docx_path = s.get_out_file(DOCX)
   document = Document(path)
   content = [p.text for p in document.paragraphs]

   txt_path = s.get_out_file(TRANSLATE)
   with open(txt_path, 'w', encoding="utf-8") as f_to:
      f_to.write("\n".join(content))

@yadopt.wrap(__doc__)
def main(args: yadopt.YadOptArgs):
   s = Script(args.book_name)
   get_document(s)

if __name__ == '__main__':
   main()