from Core.ServerAMFM import ServerAMFM
from Core.Enum.AMFM import AMFM
import pandas as pd
import pprint
import matplotlib.pyplot as plt

if __name__ == '__main__':
	print('== Конвертация  ==')
	_path = "/home/alanin/Python/Data/RawData/Servet/AM/"
	_path_conv= "/home/alanin/Python/Data/InputData/TestGPU/am00_thread_1.parquet"
	_server = ServerAMFM(_path)
	# _files = _server.read_dir_name_files()
	# _v = _server.read_file_convert(AMFM.AM, _files)
	# print(_v.head())
	# _server.write_pandas_parquet(_path_conv, _v)
	df = _server.load_pandas_parquet(_path_conv)
	# print(df.head())

	# Получаем строку по этому индексу
	print(df.loc[df['time_total'].idxmax()])
	print(df.loc[df['time_total'].idxmin()])
	print(f" mediana   {df['time_total'].median()} ")
	print(f" dispersiy   {df['time_total'].var()} ")
	print(df['time_total'])
	df['time_total'].plot(kind='box')
	plt.show()

	df_sorted = df.sort_values(by='time_total')
	pprint.pprint(df_sorted.to_dict())

	# Создание новой таблицы на основе условия
	# is_am
	# new_df = df[df['samples_num'] == 216384]
	new_df = df[(df['is_am'] == 1) & (df['samples_num'] == 216384)]
	print(new_df)
	first_3_rows = new_df.to_dict('records')
	pprint.pprint(first_3_rows)

	stop = 2

