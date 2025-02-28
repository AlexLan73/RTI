from argparse import SUPPRESS

import Core.Enum.TypePlot
from Core.Enum.AMFM import AMFM
from  Signal.Core.SignalBase0 import SignalBase0
import numpy as np
import matplotlib.pyplot as plt
import scipy.fft
from scipy.fft import fft, fftfreq, fftshift, ifft

class AMSignal(SignalBase0):
	def __init__(self, **kwargs):
		super().__init__(AMFM.AM)
		print("__ Анализируем AМ сигнал __")
		self._input_dir_base = "/home/alanin/Python/Data/OUT/AM/"
		# self._dir_data = "000"
		# self._in_args = "in_args.json"
		self._name_tfpMSeqSigns = None # "tfpMSeqSigns.json"
		# self._out_json = "out.json"
		# self._ftps_args = "ftps.json"
		self._ParserArg(**kwargs)

	def set_params_strob(self, **kwargs):
		self._ParserArg(**kwargs)


	def run(self):
		self.load_json(self._path_works_data)
		_d = self._dataOut["polar0"].Am
		self.Signal0(d=_d)
		k=1

	def Signal0(self, **kwargs):
		# self._samplesNum =  self.In_Args["samplesNum"]
		# self._shgd = self.In_Args["shgd"]
		# self._nfgdfu =  self.In_Args["nfgdfu"]
		# self._kgd =  self.In_Args["kgd"]
		#
		# _d_base = self.data[self._complex]
		self.ParserArg(**kwargs)
		ss = self._data[0:2]

		# пример по 000 директории
		_nl = self.Params["nl"]									#	4 - кол-во лучей
		_n1grs = self.Params["n1grs"]						# -3915 - смещение по частоте - отчеты с левой части
		_kgrs = self.Params["kgrs"]							#	7830 	- всего гипотиз по частоте
		_true_nihs = self.Params["true_nihs"]   # 8192 	- длинна сигнал посылки
		_nfgd_fu = self.Params["nfgd_fu"]				# -1  	- смещение гипотиз по скорости
		_kgd = self.Params["kgd"]								# 6 		- всего гипотиз по скорости
		_shgd = self.Params["shgd"]							# 2048 	- шаг гипотиз по БПФ
		_ndec = self.Params["ndec"]							# 160  	- децимация сумм сигнала
		_dlstr = self.Params["dlstr"]						# 2621439 -  размер входного строба
		_samples_num = self.Params["samples_num"] # 16384 - размер БПФ = true_nihs *2
		_nFFT = _samples_num										# размер БПФ
		_nl_num = 1
		# 1. вырезаем значение по одиному лучу
		_dx = self._data[(_nl_num-1)*_samples_num : _nl_num*_samples_num]
		_d_signal = {}
		d= self.Params["nfgd_fu"]
		v_null = _dx[:_nFFT]
		v_null[:] = 0

		for it in range(_kgd):
			d = d+it
			if d < 0:
				_x0 = np.concatenate((v_null, _dx))
				_d_signal[it]= np.abs(scipy.fft.fft(_x0[:_nFFT]))
			else:
				if d == 0:
					_d_signal[it] =_d_signal[it]= np.abs(scipy.fft.fft(_dx[:_nFFT]))
				else:
					x0 = np.tile(v_null, d)
					_x0 = np.concatenate((_dx, x0))
					_d_signal[it] =_d_signal[it]= np.abs(scipy.fft.fft(_x0[len(_x0)-_nFFT :]))




		#
		# v=np.zeros(self._samplesNum+((self._kgd+2)*self._shgd), dtype=np.complex64)
		# mas = np.zeros((self._samplesNum, self._kgd ), dtype=np.complex64)
		# mas_amp = {} # np.zeros((self._samplesNum, self._kgd ), dtype=np.float32)
		# # v = _d_base
		# if self._nfgdfu<0:
		# 	v[step:(self._samplesNum+step)] = _d_base
		# else:
		# 	v[0:self._samplesNum] = _d_base
		#
		# mas_amp = {}
		# for i in range(self._kgd):
		# 	j=i*step
		# 	mas[:, i] = v[j: j + nFFt]
		# 	v00 = v[j: j + nFFt]
		# 	_v01 = [np.sqrt(np.pow(v00[i].real, 2) + np.pow(v00[i].imag, 2))  for i in range(len(v00)) ]
		# 	mas_amp[i] = (np.array(_v01), 0)
		# 	# TypePlot.TypePlot.D2
		#
		# 	# hagm =np.abs(fft(v00))
		# 	# # hagm = hagm[:int(len(hagm)/2)]
		# 	# hagm = hagm[:20]
		# 	# mas_amp[i]=(np.array(_v01), hagm)

		self.SubPlots(TypePlot=TypePlot.TypePlot.D1Hor, d =mas_amp)
		# self.spectrum = self.WalshAll(d, nFFt, step)
		k=1