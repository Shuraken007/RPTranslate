import shutil
import os
import glob
import re
import json
from collections import OrderedDict
from tqdm import tqdm

from .utils import get_file_lines_amount
from .const import CLEAR, DUMP

def try_remove(line, json_dump, config):
   for pattern, substitution in config.items():
      report = re.findall(pattern, line, flags=re.DOTALL)
      if len(report) == 0:
         continue

      p = pattern
      if p not in json_dump:
         json_dump[p] = {}
      for founded in report:
         if founded not in json_dump[p]:
            json_dump[p][founded] = 0
         json_dump[p][founded] += 1
      line = re.sub(pattern, substitution, line, flags=re.DOTALL)
      break

   return line

def trim_file(f):
   f.seek(-1, os.SEEK_END)
   while ord(f.read(1)) in [ord(' '), ord('\n')]:
      f.seek(-2, os.SEEK_CUR)
   f.truncate()

def is_sentence_continue(line):
   if line[0].islower():
      return True
   if line[0].startswith(('.', '!', '?')):
      return True
   

def clear(script):
   book_config = script.get_book_config()
   assert(book_config.clear)

   clear_from = script.get_or_create_concat_file()
   total_lines = get_file_lines_amount(clear_from)

   file_to_path = script.get_out_file(CLEAR)
   json_dump = OrderedDict({})

   with tqdm(total=total_lines) as pbar:
      with open(clear_from, 'r') as f_from, open(file_to_path, 'wb+') as f_to:
         for line in f_from:
            pbar.update(1)
            line = try_remove(line, json_dump, book_config.clear)
            if not line:
               continue
            
            if is_sentence_continue(line):
               trim_file(f_to)
               line = ' ' + line
            f_to.write(line.encode('utf-8'))

   
   for k in json_dump.keys():
      json_dump[k] = sorted(json_dump[k].items(), key=lambda pair: pair[1], reverse=True)

   dump_file_to_path = script.get_out_file(DUMP, prefix = 'clear')
   with open(dump_file_to_path, 'w') as dump_to:
      json.dump(json_dump, dump_to, indent = 3, ensure_ascii=False)   
