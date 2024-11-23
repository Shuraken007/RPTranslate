import re
import json

FILE_IN = 'concat.txt'
FILE_OUT = 'concat_converted.txt'
FILE_DUMP = 'dump.json'

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
   json.dump(filedata, f, indent = 3)
   f.close()

def convert_splited_sentences(filedata, json_dump):
   splited_parts = re.findall(r'\n\n([a-z][^\n]+)', filedata)
   json_dump['splited_parts'] = splited_parts

   filedata = re.sub(r'\n\n([a-z])', r' \1', filedata)

   return filedata

def convert_file():
   filedata = get_filedata(FILE_IN)
   json_dump = {}

   filedata = convert_splited_sentences(filedata, json_dump)

   set_filedata(filedata, FILE_OUT)
   set_dump(FILE_DUMP, json_dump)
   # print(json_dump)

if __name__ == '__main__':
   convert_file()