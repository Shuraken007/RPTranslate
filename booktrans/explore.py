import shutil
import os
import glob
from googletrans_di import Translator
import json
import re
from collections import OrderedDict

from .utils import build_path
from .const import DUMP, MAX_TRANSLATE_LEN

def get_proper_nouns(script):
   explore_from = script.get_or_create_concat_file()

   proper_nouns = {}
   with open(explore_from, 'r') as f_from:
      for line in f_from:
         words = re.findall(r'[^.]\s([A-Z]\w+\s*?)+', line)
         for w in words:
            if w not in proper_nouns:
               proper_nouns[w] = {'n': 0}
            proper_nouns[w]['n'] += 1

   proper_nouns = dict(filter(lambda x: x[1]['n'] > 5, proper_nouns.items()))
   proper_nouns = OrderedDict(sorted(proper_nouns.items(), key=lambda x: x[1]['n'], reverse=True))
   return proper_nouns

def translate(proper_nouns):
   translator = Translator()
   for k, v in proper_nouns.items():
      text_translate = translator.translate(k, dest='ru', src='en')
      v['t'] = text_translate.text
      v['e'] = text_translate.extra_data

def explore(script):
   dump_file_to_path = script.get_out_file(DUMP, prefix = 'explore')
   json_dump = {}

   proper_nouns = get_proper_nouns(script)
   translate(proper_nouns)

   json_dump = {'proper_nouns': proper_nouns}
   for k, v in json_dump['proper_nouns'].items():
      json_dump['proper_nouns'][k] = str(v)

   with open(dump_file_to_path, 'w') as dump_to:
      json.dump(json_dump, dump_to, indent = 3, ensure_ascii=False)