from pathlib import Path
import os

def build_path(path_arr, file_name=None, mkdir=False):
   path = os.path.join(os.path.dirname( __file__ ), '..', *path_arr)
   if mkdir:
      Path(path).mkdir(parents=True, exist_ok=True)
   if file_name:
      path = os.path.join(path, file_name)
   elif not path.endswith(os.path.sep):
      path += os.path.sep
   return path

def change_file_name(file_path, name):
   path, filename = os.path.split(file_path)
   newpath = os.path.join(path, name)
   return newpath

def get_file_lines_amount(file_path):
   with open(file_path, 'rb') as f:
      lines = 0
      buf_size = 1024 * 1024

      buf = f.raw.read(buf_size)
      while buf:
         lines += buf.count(b'\n')
         buf = f.raw.read(buf_size)
         
   return lines   