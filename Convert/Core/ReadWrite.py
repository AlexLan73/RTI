import os
import os.path
import pickle
import pandas as pd
import numpy as np
import json
import re
import pandas as pd

from functools import wraps

def handle_file_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print(f"Файл {args[1]} не найден.")
            raise ValueError(f"Файл {args[1]} не найден.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            raise
    return wrapper


class ReadWrite:
	def __init__(self):
		self.pathStatistik = "/home/alanin/Python/Data/Statistik/"
		self.path_report = "/home/alanin/Python/Data/TestGPU/"
		self.ext_pandes = ".parquet"
		self.ext_exsel = ".xlsx"

	@handle_file_errors
	def load_json(self, path):
		with open(path, 'r', encoding='utf-8') as file:
			return json.load(file)


	def write_json(self, path, data):
		with open(path, 'w', encoding='utf-8') as file:
			json.dump(data, file)


	@handle_file_errors
	def load_pickle(self, path):
		with open(path, 'rb') as file:
			return pickle.load(file)


	def write_pickle(self, path, data):
		with open(path, 'wb') as file:
			pickle.dump(data, file)


	@handle_file_errors
	def load_txt(self, path):
		with open(path, 'rb') as file:
			return file.read()

	@handle_file_errors
	def load_txt_line(self, path):
		with open(path, 'rb') as file:
			return file.readlines()

	def write_txt(self, path, data):
		with open(path, 'wb') as file:
			file.write(data)

	def write_pandas_to_excel(self, name_file, pd):
		pd.to_excel(f"{self.pathStatistik}/{name_file}.xlsx", index=False)

	'''
	Сохранение в формате Parquet: (Эффективный бинарный формат)

	python
	df.to_parquet('my_data.parquet', index=False)  
	Сначала вам может понадобиться установить библиотеку pyarrow: pip install pyarrow 
	(иногда fastparquet тоже может потребоваться pip install fastparquet)
	Parquet - это колоночный формат хранения данных, оптимизированный для запросов и аналитики. 
	Он часто используется для больших наборов данных.

	'''
	def _replace_path_parquet(self, path):
		_path = str(path)
		_path = self.path_report+_path.replace(self.path_report, "")
		_path = _path.replace(self.ext_pandes, "")+self.ext_pandes
		return _path

	@handle_file_errors
	def load_pandas_parquet(self, path):
		_path = self._replace_path_parquet(path)
		return pd.read_parquet(_path)

	def write_pandas_parquet(self, path, df):
		_path = self._replace_path_parquet(path)
		df.to_parquet(_path, index=False)


