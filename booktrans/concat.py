import shutil
import os
import glob

from .utils import build_path
from .const import INPUT, CHAPTER_DELIM, CONCAT

def concat(script):
   file_to_path = script.get_out_file(CONCAT)
   glob_from_path = build_path([INPUT, script.book_name], '*.txt')

   with open(file_to_path, 'wb') as f_to:
      for filename in glob.glob(glob_from_path):
         with open(filename, 'rb') as f_from:
            shutil.copyfileobj(f_from, f_to)
         f_to.write(b"\n" + CHAPTER_DELIM.encode('utf-8') + b"\n")