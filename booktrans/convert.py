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

blocks_config = OrderedDict({
   r'\n(Глава.*?)\s*\[.*?Amazon.*?\].*?': r'\1',
   r'\n(.*?Amazon.*?)\n': '',
   r'\n(.*?автор.*?)\n': '',
   r'\n(.*?Royal Road.*?)\n': '',
   r'\n(.*?Королевск.*?дорог.*?)\n': '',
   r'\n(.*?Украд.*?;.*?)\n': '',
})

def remove_blocks(filedata, json_dump):
   replaced = {}
   for k, v in blocks_config.items():
      report = re.findall(k, filedata)
      replaced[k] = set()
      for f in report:
         replaced[k].add(f)
      replaced[k] = list(replaced[k])

      filedata = re.sub(k, v, filedata)
   
   json_dump['replaced_blocks'] = replaced
   return filedata

words_config = OrderedDict({
   r'Arbitage': "Арбитаж(!)",
   r'Arbitrage': "Арбитаж(!)",
   r'Silvertide': "Сильвертид(!)",
   r'Серебрян.*? (?:П|п)рилив': "Сильвертид(!)",
   r'Aylin': "Эйлин(!)",
   r'advanced track': "продвинутой группы(!)",
   r'((?:П|п)родвинут[а-я\s]*?)трек': r"\1группа(!)",
   r'Renewal|Обновление|Ренессанс|Возобновление|Продление': "Возрождение(!)",
   r'I\'m': "Я(!)",
   r'Evergreen': "Эвергрин(!)",
   r'Wizen': "Визен(!)",
   r'Ноа': "Ной",
   r'(?:Т|т)алисман': "Маскот",
   r'Ул': "Ули",
   r'Эйзел': "Айзел",
})

def get_sentence_for_pattern(pattern, filedata):
   wrapped_pattern = r'.[^А-ЯA-Z\n.!?]*?' + pattern + r'.*?(?:\.|!|\?|\n)'
   report = re.findall(wrapped_pattern, filedata)
   return report

def replace_words(filedata, json_dump):
   replaced = {}
   for k, v in words_config.items():
      replaced[k] = get_sentence_for_pattern(k, filedata)
      filedata = re.sub(k, v, filedata)
   
   json_dump['replaced_words'] = replaced
   return filedata

def convert_file(filedata, json_dump):
   filedata = remove_unreadables(filedata, json_dump)
   filedata = remove_blocks(filedata, json_dump)
   filedata = replace_words(filedata, json_dump)
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
   split_on_files(filedata, json_dump)

   set_filedata(filedata, FILE_OUT)
   set_dump(FILE_DUMP, json_dump)
