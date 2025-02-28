import re

import numpy as np
import matplotlib.pyplot as plt
import statistics



def parse_numbers_from_file(filename):
	with open(filename, 'r') as file:
		lines = file.readlines()

	k = 0
	_d = {}
	numbers = []
	for it in range(1, len(lines)):
		# Удаляем перевод строки
		line = lines[it].strip()
		_lineS = re.sub(r'\s+', ' ', line).split(" ")
		_d_info = {}
		_d_info["file"] = _lineS[0]
		_d_info["samples"] = int(_lineS[4])
		_d_info["time_full"] = float(_lineS[7])
		_d_info["time_fft"] = float(_lineS[8])
		_d[k] = _d_info
		k+=1
	return _d


def _parser_data(data):
	_d_time = [(val["samples"], val["time_full"], val["time_fft"]) for val in data.values()]
	_xsamp = [x[0] for x in _d_time]
	_full = [x[1] for x in _d_time]
	_fft = [x[2] for x in _d_time]
	return _xsamp, _full, _fft



def plotTime(data, _name_fmam):
	_xsamp, _full, _fft = _parser_data(data)
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
	_xsamp, _full, _fft = _parser_data(data)
	_proc = [_full[i]/_fft[i] for i in range(len(_full))]
	fig, ax = plt.subplots()
	# Строим график точками
	ax.plot(_xsamp, _proc, marker='o', linestyle='None')
	plt.title(f'График {_name_fmam} отчеты samples и full/fft')
	# Устанавливаем логарифмический масштаб по оси X
	ax.set_xscale('log')

	# Устанавливаем заголовки осей
	ax.set_xlabel('samples')
	ax.set_ylabel('отношение full/fft')
	plt.grid()
	# Показываем график
	plt.show()

def plot_median_time(data):
	_xsamp, _full, _fft = _parser_data(data)
	_d = {}
	for i in range(len(_xsamp)):
		_ix = _xsamp[i]
		_vfull = _fft[i]
		_vfft = _fft[i]

		# if _ix in _d.keys():
		# 	_xsamp[_ix].append()
		# else:
		# 	_xsamp[_ix]={}
		# 	_xsamp[_ix]



if __name__ == '__main__':
	print('== Тест производительности ==')
	#
	# # Пример списка чисел
	# numbers = [1, 3, 3, 6, 7, 8, 9]
	# # Расчет медианы
	# median_value = statistics.median(numbers)
	# print("Медиана:", median_value)
	# print("средняя :", sum(numbers)/len(numbers))

	_name_fmam = "FM"
	filename = "/home/alanin/Python/Data/TestGPU/report_fm_00.txt"
	# filename = "/home/alanin/Python/Data/TestGPU/report_am_00.txt"
	data = parse_numbers_from_file(filename)
	plotTime(data, _name_fmam)
	plot_proce(data, _name_fmam)


