import shutil
import os
import glob
from googletrans_di import Translator
import json
import re
from tqdm import tqdm

from .utils import get_file_lines_amount
from .const import TRANSLATE, DUMP, MAX_TRANSLATE_LEN, EXTRACT_LEN_ON_FAIL, REPLACE_BEFORE

def dump_translate_obj(text_orig, translate_obj, file, is_debug):
   if not is_debug:
      return
   json_data = {
      'orig': text_orig,
      'trans': translate_obj.text,
      # 'extra': translate_obj.extra_data
   }
   json.dump(json_data, file, indent = 3, ensure_ascii=False)

def extract_from_arr_by_length(arr_from, arr_to, length):
   extr_len = 0
   while extr_len < length and len(arr_from) > 0:
      extracted = arr_from.pop()
      extr_len += len(extracted)
      arr_to.append(extracted)

def translate_arr(arr, translator, f_to, dump_to, is_debug, pbar):
   extra = []
   while(True):
      text_orig = ''.join(arr)
      translate_obj = translator.translate(text_orig, dest='ru', src='en')

      # normally this condition shouldn't run, if we send too much data
      # text won't be translated
      # so we must reduce amount of data and try again, giant loss of time
      if len(translate_obj.extra_data["translation"][0]) == 4:
         extract_from_arr_by_length(arr, extra, EXTRACT_LEN_ON_FAIL)
         continue
      
      pbar.update(len(arr))
      dump_translate_obj(text_orig, translate_obj, dump_to, is_debug)
      if not translate_obj.text.endswith('\n'):
         translate_obj.text += '\n'
      f_to.write(translate_obj.text)
      cur_len = 0
      break
   return extra

def translate(script):
   is_debug = True
   translate_from = script.get_out_file(REPLACE_BEFORE)
   total_lines = get_file_lines_amount(translate_from)

   file_to_path = script.get_out_file(TRANSLATE)
   dump_file_to_path = script.get_out_file(DUMP, prefix = 'translate')

   translator = Translator()
   
   with tqdm(total=total_lines) as pbar:
      with open(translate_from, 'r') as f_from, \
            open(file_to_path, 'w') as f_to, \
            open(dump_file_to_path, 'w') as dump_to:
         text = []
         cur_len = 0
         for line in f_from:
            if cur_len + len(line) > MAX_TRANSLATE_LEN:
               text = translate_arr(text, translator, f_to, dump_to, is_debug, pbar)

               cur_len = 0

            text.append(line)
            cur_len += len(line)

         while len(text) > 0:
            text = translate_arr(text, translator, f_to, dump_to, is_debug, pbar)