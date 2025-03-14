import re

import numpy as np
import matplotlib.pyplot as plt
import statistics

from Convert.Core.ConvertTo import ConvertTo
from Convert.Core.ReadWrite import ReadWrite


def plotTime(data, _name_fmam):
	# _xsamp, _full, _fft = _parser_data(data)
	_xsamp = data["xsamp"]
	_full = data["full"]
	_fft = data["fft"]

	fig, ax = plt.subplots()
	# Строим график точками
	ax.plot(_xsamp, _full, _xsamp, _fft, marker='o', linestyle='None')
	plt.title(f'График {_name_fmam} отчеты samples и время выполнение - Full fft время')
	# Устанавливаем логарифмический масштаб по оси X
	ax.set_xscale('log')

	# Устанавливаем заголовки осей
	ax.set_xlabel('samples')
	ax.set_ylabel('time')
	plt.grid()
	# Показываем график
	plt.show()

def plot_proce(data, _name_fmam):
	# _xsamp, _full, _fft = _parser_data(data)
	_xsamp = data["xsamp"]
	_full = data["full"]
	_fft = data["fft"]

	_fulla = np.array(_full)
	_ffta = np.array(_fft)
	_proc = (_fulla - _ffta)/ _fulla

	fig, ax = plt.subplots()
	# Строим график точками
	ax.plot(_xsamp, _proc, marker='o', linestyle='None')
	plt.title(f'График {_name_fmam} отчеты samples и % времени загрузки от общего времени (full-fft)/full ' )
	# Устанавливаем логарифмический масштаб по оси X
	ax.set_xscale('log')

	# Устанавливаем заголовки осей
	ax.set_xlabel('samples')
	ax.set_ylabel('отношение (full-fft)/full')
	plt.grid()
	# Показываем график
	plt.show()

def plot_median_time(data):
	_xsamp = data["xsamp"]
	_full = data["full"]
	_fft = data["fft"]
	_d = {}
	# _xsamp, _full, _fft = _parser_data(data)
	_d_fft = {}
	_d_full = {}
	_d_fft_med = {}
	_d_full_med = {}
	for i in range(len(_xsamp)):
		_ix = _xsamp[i]
		if not(_ix in _d_fft.keys()):
			_d_fft[_ix] = []
			_d_full[_ix] = []
		_d_fft[_ix].append(_fft[i])
		_d_full[_ix].append(_full[i])

	_d_fft_med = {key: statistics.median(val) for key, val in _d_fft.items()}
	_d_fft_med =dict(sorted(_d_fft_med.items()))

	# for key, val in _d_fft.items():
	# 	_d_fft_med[key] = statistics.median(val)
	# _d_fft_med =dict(sorted(_d_fft_med.items()))
	_d_full_med = {key: statistics.median(val) for key, val in _d_full.items()}
	_d_full_med = dict(sorted(_d_full_med.items()))

	#
	# for key, val in _d_full.items():
	# 	_d_full_med[key] = statistics.median(val)
	# _d_full_med = dict(sorted(_d_full_med.items()))

	kkk=1

if __name__ == '__main__':
	""" Данные из txt файла  """
	print('== Тест производительности ==')

	_name_fmam = "AM"
	file_pickl_base = "/home/alanin/Python/Data/TestGPU/"

	_name_pickle = "am01"
	_convert = ConvertTo()
	# data = _convert.txt_test_gpu0(filename)
	# _convert.write_pickle(file_pickl_base+_name_pickle+".pickle", data)
	data = _convert.load_pickle(file_pickl_base+_name_pickle+".pickle")
	# plotTime(data, _name_fmam)
	# plot_proce(data, _name_fmam)
	plot_median_time(data)



	# filename = "/home/alanin/Python/Data/InputData/TestGPU/report_fm_00.txt"
	# filename = "/home/alanin/Python/Data/InputData/TestGPU/report_am_00.txt"


