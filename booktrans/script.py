import os
import importlib.util
import sys

from .utils import build_path
from .const import OUTPUT, INPUT, CONCAT, CLEAR, TRANSLATE, DUMP
from .concat import concat

class Script:
   def get_book_config(self):
      path = build_path([INPUT, self.book_name], 'config.py')
      if not os.path.exists(path):
         raise Exception(f'file {path} not existed')
         
      book_spec = importlib.util.spec_from_file_location("config", path)
      book_config = importlib.util.module_from_spec(book_spec)
      sys.modules["config"] = book_config
      book_spec.loader.exec_module(book_config)
      return book_config

   def validate_book(self, name):
      assert(name is not None)
      path = build_path([INPUT, name])
      if not os.path.exists(path):
         raise Exception(f'path {path} not existed')

   def get_out_file(self, name, prefix=None):
      file_name = name
      if prefix:
         file_name = f'{prefix}_{name}'
      return build_path([OUTPUT, self.book_name], file_name, mkdir=True)

   def get_or_create_concat_file(self):
      path = build_path([OUTPUT, self.book_name], CONCAT)
      if not os.path.exists(path):
         print(f'file {path} not founded, running concatenation')
         concat(self)
      return path

   def __init__(self, book_name):
      self.validate_book(book_name)
      self.book_name = book_name