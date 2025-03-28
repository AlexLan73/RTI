import os
import re
from os import remove

import pandas as pd
from pathlib import Path
from typing import Union, Dict, Any

from Convert.Core.ComparisonData import ComparisonData
from Convert.Core.ReadWrite import ReadWrite
from Core.Enum import AMFM

import seaborn as sns
import matplotlib.pyplot as plt

class ServerAMFM(ReadWrite, ComparisonData):
	def __init__(self, *args):
		super().__init__()
		ComparisonData.__init__(self)
		self._path_input = None
		self._path_output = None
		self._df = None
		self._dfs = None

		self.d_path={}
		self.data_df={}

		if args.__len__()>0:
			self._path_input = args[0]
			if not os.path.exists(self._path_input):
				raise FileNotFoundError(f"Нет такого файла: {self._path_input}")

			try:
				self._path_output = args[1]
			except:
				pass


	# amfm: AMFM
	"""  Читаем файлы из директорий   """
	def read_dir_name_files(self, path:str=None):
		if path is None:
			path = self._path_input

		if not os.path.exists(path):
			raise FileNotFoundError(f"Нет такого файла: {path}")

		# Пример использования
		directory_path = path
		files = self.get_file_paths_pathlib(directory_path)
		for file_path in files:
			print(file_path)
		return files

	"""  Возвращает список полных путей ко всем файлам в указанном каталоге (используя pathlib). """
	def get_file_paths_pathlib(self, directory):
			return [str(entry) for entry in Path(directory).iterdir() if entry.is_file()]
			# directory_path = Path(directory)
			# return [str(entry) for entry in directory_path.iterdir() if entry.is_file()]

	"""  Рекурсивно возвращает список путей ко всем файлам (pathlib).  """
	def get_all_file_paths_pathlib(self, directory):
			return [str(entry) for entry in Path(directory).rglob("*") if entry.is_file()]
			# directory_path = Path(directory)
			# return [str(entry) for entry in directory_path.rglob("*") if entry.is_file()]

	"""  Читаем файлы с данными (json) и конвертируем в словарь затем в pandas.  """
	def read_file_convert(self, amfm: AMFM, path_files:list):
		data_json=[]
		kk=0
		for it in path_files:
			kk = kk+1
			print(f" N- {kk}    file -> {it}  ")
			file_size = os.path.getsize(it)
			if file_size == 0:
				print("---  размер файла = 0")
				continue
			v = self.load_json(it)
			data_json.append(v)   # список со значениями для формирования словаря и базы

		# поля в будущей базе pandas
		ls_name = ["report_path", "N", "nl", "n1grs", "kgrs", "true_nihs", "nfgd_fu", "kgd", "shgd", "samples_num",
							 "is_am", "sum_samples", "time_total", "time_sine", "time_start", "time_end"]
		d={it:[] for it in ls_name }

		d["time_fft"] = []
		d["time_read"] = []
		d["time_write"] = []

		# разбор json
		for it in data_json:
			__path = it["report_path"]
			d["report_path"].append(__path)
			match = re.search(r'\d+', __path)
			number = -1
			if match:
				number = int(match.group(0))

			d["N"].append(number)
			__nl = it["params"]["nl"]
			d["nl"].append(__nl)
			d["n1grs"].append(it["params"]["n1grs"])
			d["kgrs"].append(it["params"]["kgrs"])
			d["true_nihs"].append(it["params"]["true_nihs"])
			d["nfgd_fu"].append(it["params"]["nfgd_fu"])
			d["kgd"].append(it["params"]["kgd"])
			d["shgd"].append(it["params"]["shgd"])

			__samples_num = it["params"]["samples_num"]
			d["samples_num"].append(__samples_num)
			d["sum_samples"].append(__nl * __samples_num)
			d["is_am"].append(it["params"]["is_am"])
			__total = it["time"]["total"]["duration"]
			__time_start0 = it["time"]["cpu_start_point"]
			__time_start = __time_start0 # pd.to_datetime(it["time"]["start"], format="%d.%m.%Y %H:%M:%S")
			__time_end = __time_start0 # __time_start + pd.Timedelta(milliseconds=__total)
			d["time_start"].append(__time_start)
			d["time_end"].append(__time_end)

			d["time_sine"].append(it["time"]["sine"]["duration"])
			d["time_total"].append(__total)
			d["time_fft"].append(it["time"]["fft"]["duration"])
			d["time_read"].append(it["time"]["read_data"]["duration"])
			d["time_write"].append(it["time"]["write_data"]["duration"])

		self._df = pd.DataFrame(d)
		return self._df

	def find_path_data(self, path, amfm:AMFM, maska_dir=None):
		if maska_dir == None:
			print(" --  не указана maska_dir  -- ")
			raise " --  error -> maska_dir=None  -- "

		json_files = []
		root_dir = Path(path)
		for reports_dir in root_dir.rglob(maska_dir):
			if reports_dir.is_dir():
				json_files.extend([str(path) for path in reports_dir.rglob('*.json')])

		return self.read_file_convert(amfm, json_files)

	''' Грузим данные в pandas  '''
	def load_pandas(self, _path_conv: Union[str, Path, Dict[str, Union[str, Path]], Any]) -> None:
		if isinstance(_path_conv, (str, Path)):
			""" один путь """
			self._df = self.load_pandas_parquet(str(_path_conv))
		elif isinstance(_path_conv, dict):
			""" словарь с путями """
			self._dfs = {}
			for key, val in _path_conv.items():
				self._dfs[key] = self.load_pandas_parquet(str(val))
		else:
			raise TypeError(f"Unsupported type: {type(_path_conv)}")

	''' расчет одной базы '''
	def midel_time(self):
		ls_num_group = sorted(self._df['N'].unique())

		# Удаление нескольких столбцов
		# columns_to_drop = ['time_sine', 'time_start', 'time_end']  #
		# ["N", "nl", "n1grs", "kgrs","kgd", "shgd", "samples_num",
		#  "is_am", "sum_samples", "time_total", "time_sine", "time_start", "time_end"]

		columns_to_drop = ["report_path",  "true_nihs", "nfgd_fu", "sum_samples",
											 'time_sine', 'time_end']  #  'time_start',
		self._df = self._df.drop(columns_to_drop, axis=1)

		grouped_result = self._df.groupby('N').agg({
			"time_total": 'median',
			"time_fft": 'median'
		})
		grouped_result = grouped_result.sort_values(by='time_total')

		_dv = self._df[self._df["is_am"]==0]  #self._df["time_total"]>0.0
		_dv_kgrs = _dv[(((self._df["nl"]==5) & (self._df["kgrs"]==60))
										|(self._df["nl"]==10) & (self._df["kgrs"]==15) )& (self._df["kgd"] == 2046) ]


		_dv_kgrs = _dv_kgrs.sort_values(by='time_total')    #'time_total'
		_dv0 = _dv.sort_values(by='N')
		_dv00 = _dv.groupby('N').agg({
			"time_total": 'median',
			"time_fft": 'median'
		})

		# _dv_am = self._df[(self._df["is_am"]==1) & (self._df["N"]==62)]
		# _dv_fm5 = self._df[(self._df["is_am"]==0) & (self._df["N"]==0)]
		_dv_0 = _dv.sort_values(by='time_total')

		_dv_0['rez'] = (1 - _dv_0["time_fft"] / _dv_0["time_total"].replace(0, 1e-9)) * 100  # Заменяем 0 на очень маленькое число
		_dv_1 = _dv_0.sort_values(by='rez')

		# Группировка по столбцу 'Category' и вычисление дисперсии для каждой группы
		std_time_total = self._df[(self._df["is_am"]==0)].groupby('N')['time_total'].std()  # var - медиана
		std_time_fft = self._df[(self._df["is_am"]==0)].groupby('N')['time_fft'].std()

		grouped_result = self._df[(self._df["is_am"]==0) ].groupby('N').agg({
			"time_total": 'std',
			"time_fft": 'std',
			"time_write": 'std'
		})  #.dropna(how='all')
		median_grouped_result = self._df[(self._df["is_am"]==0) ].groupby('N').agg({
			"time_total": 'var',
			"time_fft": 'var',
			"time_write": 'var'
		})  #.dropna(how='all')

		# grouped_kgrs = self._df[(self._df["is_am"]==0) ].groupby('kgrs').apply(lambda x: x.to_dict('list'))

		# for index, row in grouped.iterrows():
		# 	print(f"{index}: {row['Value1']} {row['Value2']}")

		grouped_result_var = self._df[(self._df["is_am"]==0) ].groupby('N').agg({
			"time_total": 'var',
		})  #.dropna(how='all')

		# "time_read": 'std',

		grouped_result0 = grouped_result[grouped_result["time_total"]>5]

		_dv_am = self._df[(self._df["is_am"]==0) ]
		_dv_am_sort = _dv_am.sort_values(by='time_total')
		columns_to_drop = ["is_am", "n1grs", "time_start"]  #  'time_start',
		_dv_am_sort = _dv_am_sort.drop(columns_to_drop, axis=1)
		self.write_pandas_to_excel("n1_sort_time", _dv_am_sort)
		# _dv_am_sort.to_excel('n1_time_total.xlsx', index=False)
		# v = _dv_am[]   & (self._df["N"]==23)
		# _dv_am = self._df[self._df["is_am"]==1 & self._df["N"]==0]
		# ls_time_total = sorted(grouped_result['time_total'])
		# grouped_result = self._df.groupby('N').agg({
		# 	"time_total": 'mean',
		# 	"time_fft": 'median'
		# })

		# Сохраняем результаты в новую таблицу
		# grouped_result.to_csv('result.csv', index=True)
		k=1

	def load_data_dict(self, path_data):
		self.d_path = path_data
		for key, val in self.d_path.Items():
			self.data_df[key]= self.load_pandas_parquet(val)

	def comparison_of_streams(self):
		_ls = list(self._dfs.keys())
		del _ls[0]
		v_test = self._dfs[_ls[0]]
		v_test = v_test[(v_test["is_am"]==0)]
		new_df = v_test.groupby('N')[['nl', 'kgrs', "kgd", "samples_num"]].first().reset_index()
		d0 ={}
		d1 = {}
		dall=new_df
		for it in  _ls:
			_pref = str(it).replace("n", "t")+"_"
			v_test = self._dfs[it]
			vdf = self.del_field_all(v_test[(v_test["is_am"] == 0)])
			vv = self.form_data_var_std(vdf)
			vv.columns = [x if "N" in x else _pref+x for x in vv.columns]
			d0[it] = vv
			d1[it] = pd.concat([new_df, vv], axis=1)
			for key_time in vv.columns:
				if ('total' in  key_time) | ('fft' in  key_time):
					dall[key_time]=vv[key_time]

		for key, val in d1.items():
			_name_file = str(key).replace("n", "t")+"streams"
			self.write_pandas_to_excel(_name_file, val)

		self.write_pandas_to_excel("streams_all", dall)

	def comparison_of_nikolay(self):
		_ls_df = self._df.groupby('N').first().reset_index()
		_ls_n = _ls_df["N"].tolist()
		_d0 ={}
		for it in _ls_n:
			v =  self._df[self._df["N"]==it]
			v1 = self.del_field_N_sum_samples(v)
			_d0[it]=v1

		_d1={}
		for key, val in _d0.items():
			_d0_kgrs = {}
			_ls_kgrs = val["kgrs"].unique().tolist()
			_ls_kgrs.sort()
			for it_kgrs in _ls_kgrs:
				vv00 = val[val["kgrs"]==it_kgrs]
				vv00 = self.del_field_kgrs(vv00.reset_index())
				_d0_kgrs[it_kgrs]= vv00
			_d1[key] = _d0_kgrs

		k=1

	def ComvertToExcel(self, param):
		_path = param

		v0 = self.form_data_var_std_ls(self._df, ['N', 'kgrs'])

		# self._df.columns = [x if not("time_" in x) else str(x).replace("time_", "") for x in self._df.columns]
		new_df = self._df.groupby(['N', 'kgrs'])[['nl', "kgd", "samples_num"]].first().reset_index()

		vx0 = pd.concat([new_df, v0], axis=1)


		# v = self.del_field_is_am(self._df)
		# v = self.form_data_var_std(v)
		# vx0 = vx0.sort_values(by='total_mean')
		self.write_pandas_to_excel(_path, vx0)
		stop=1


# v_test.groupby('N')[['nl', 'kgrs', "kgd", "samples_num"]].first().reset_index()
# v_test = self._dfs[_ls[0]]
# v_test = v_test[(v_test["is_am"]==0)]
# new_df = v_test.groupby('N')[['nl', 'kgrs', "kgd", "samples_num"]].first().reset_index()

