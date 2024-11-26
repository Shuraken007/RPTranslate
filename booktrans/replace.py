import shutil
import os
import glob
from googletrans_di import Translator
import json
import re
from collections import OrderedDict

from .utils import build_path
from .const import CLEAR, REPLACE_BEFORE, REPLACE_AFTER, TRANSLATE

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

def replace_before(script):
   book_config = script.get_book_config()
   assert(book_config.replacements)
   r_pref = book_config.replace_prefix
   r_post = book_config.replace_postfix
   assert(r_pref)
   assert(r_post)
   save_r_pref = book_config.not_prefix_tmp_replace
   save_r_post = book_config.not_postfix_tmp_replace
   assert(save_r_pref)
   assert(save_r_post)

   replace_from = script.get_out_file(CLEAR)
   if not os.path.exists(replace_from):
      raise Exception(f'path {path} not existed')

   file_to_path = script.get_out_file(REPLACE_BEFORE)

   with open(replace_from, 'r') as f_from, open(file_to_path, 'w') as f_to:
      for line in f_from:
         line = line.replace(r_pref, save_r_pref)
         line = line.replace(r_post, save_r_post)
         for k, v in book_config.replacements.items():
            if k in line:
               replacement = v['t']
               if 'context' in v:
                  replacement += r_pref+v['context']+r_post
               line = line.replace(k, replacement)
         f_to.write(line)

def replace_after(script):
   book_config = script.get_book_config()
   r_pref = book_config.replace_prefix
   r_post = book_config.replace_postfix
   assert(r_pref)
   assert(r_post)
   save_r_pref = book_config.not_prefix_tmp_replace
   save_r_post = book_config.not_postfix_tmp_replace
   assert(save_r_pref)
   assert(save_r_post)

   replace_from = script.get_out_file(TRANSLATE)
   if not os.path.exists(replace_from):
      raise Exception(f'path {path} not existed')

   file_to_path = script.get_out_file(REPLACE_AFTER)

   with open(replace_from, 'r') as f_from, open(file_to_path, 'w') as f_to:
      for line in f_from:
         regexp = "{}.*?{}" .format(re.escape(r_pref), re.escape(r_post))
         line = re.sub(regexp, '', line)
         line = line.replace(r_pref, '')
         line = line.replace(r_post, '')
         line = line.replace(save_r_pref, r_pref)
         line = line.replace(save_r_post, r_post)

         f_to.write(line)
