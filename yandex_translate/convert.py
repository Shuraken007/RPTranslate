import re
import json
import string
from collections import OrderedDict
from pathlib import Path
import os

FILE_IN = 'translate.txt'
FILE_OUT = 'translate_converted.txt'
FILE_DUMP = 'dump.json'
FOLDER_OUT = 'split'

def get_filedata(file):
   f = open(file,'r')
   filedata = f.read()
   f.close()
   return filedata

def set_filedata(filedata, file):
   with open(file, 'w') as f:
      f.write(filedata)

def set_dump(file, filedata):
   f = open(file,'w')
   json.dump(filedata, f, indent = 3, ensure_ascii=False)
   f.close()

def remove_unreadables(filedata, json_dump):
   unreadables = {}
   allowed = ['\n']
   for c in filedata:
      if c.isprintable() or c in allowed:
         continue
      if not c in unreadables:
         unreadables[c] = 0
      unreadables[c] += 1
   
   dd = {ord(c):None for c in unreadables.keys()}
   json_dump['unreadables'] = unreadables

   return filedata.translate(dd)

engChar = re.compile(r'[a-zA-Z]')
def check_other_lang(filedata, json_dump):
   not_english_words = {}
   words = [w.strip(string.punctuation) for w in filedata.split()]
   for w in words:
      for c in w:
         if c.isalpha() and engChar.match(c):
            if w not in not_english_words:
               not_english_words[w] = 0
            not_english_words[w] += 1
            break
   json_dump['not_english'] = sorted(not_english_words.items(), key=lambda pair: pair[1], reverse=True)

replace_config = OrderedDict({
   r'\n(Глава.*?)\s*\[.*?Amazon.*?\].*?': r'\1',
   r'\n(.*?Amazon.*?)\n': '',
   r'\n(.*?автор.*?)\n': '',
   r'\n(.*?Royal Road.*?)\n': '',
   r'\n(.*?Королевск.*?дорог.*?)\n': '',
   r'((?:[А-Я]|\n|\s).*?)Arbitage(.*?\.|\n)': r'\1Арбитраж(!)\2',
   r'((?:[А-Я]|\n|\s).*?)Arbitrage(.*?\.|\n)': r'\1Арбитраж(!)\2',
   r'((?:[А-Я]|\n|\s).*?)Silvertide(.*?\.|\n)': r'\1Сильвертид(!)\2',
   r'((?:[А-Я]|\n|\s).*?)Серебрян.*? (?:П|п)рилив(.*?\.|\n)': r'\1Сильвертид(!)\2',
   r'((?:[А-Я]|\n|\s).*?)Aylin(.*?\.|\n)': r'\1Эйлин(!)\2',
   r'((?:[А-Я]|\n|\s).*?)advanced track(.*?\.|\n)': r'\1продвинутой группы(!)\2',
   r'((?:[А-Я]|\n|\s).*?)Renewal(.*?\.|\n)': r'\1Возрождение(!)\2',
   r'((?:[А-Я]|\n|\s).*?)Обновление(.*?\.|\n)': r'\1Возрождение(!)\2',
   r'((?:[А-Я]|\n|\s).*?)I\'m(.*?\.|\n)': r'\1Я(!)\2',
   r'((?:[А-Я]|\n|\s).*?)Evergreen(.*?\.|\n)': r'\1Эвергрин(!)\2',
   r'((?:[А-Я]|\n|\s).*?)Wizen(.*?\.|\n)': r'\1Визен(!)\2',
})

def replace_data(filedata, json_dump):
   replaced = {}
   for k, v in replace_config.items():
      report = re.findall(k, filedata)
      replaced[k] = set()
      for f in report:
         replaced[k].add(f)
      replaced[k] = list(replaced[k])

      filedata = re.sub(k, v, filedata)
   
   json_dump['replaced'] = replaced
   return filedata

def convert_file(filedata, json_dump):
   filedata = remove_unreadables(filedata, json_dump)
   filedata = replace_data(filedata, json_dump)
   check_other_lang(filedata, json_dump)
   return filedata
   # print(json_dump)

re_chapter = re.compile("Глава (\d+)\:")
def split_on_files(filedata, json_dump):
   if not os.path.exists(FOLDER_OUT):
      os.makedirs(FOLDER_OUT)   

   filedata = filedata.strip()
   last_num, num, f = None, None, None
   for line in filedata.split("\n"):
      if match := re_chapter.match(line):
         num = match.group(1)
      if last_num != num:
         if f:
            f.close()
         file_path = os.path.join(FOLDER_OUT, f'{num}.txt')
         f = open(file_path, 'w')
         last_num = num
      print(line, file=f)
   
   if f:
      f.close()

if __name__ == '__main__':
   filedata = get_filedata(FILE_IN)
   json_dump = {}

   filedata = convert_file(filedata, json_dump)
   # split_on_files(filedata, json_dump)

   set_filedata(filedata, FILE_OUT)
   set_dump(FILE_DUMP, json_dump)
