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
		k=1

	def Signal0(self):
		self._samplesNum =  self.In_Args["samplesNum"]
		self._shgd = self.In_Args["shgd"]
		self._nfgdfu =  self.In_Args["nfgdfu"]
		self._kgd =  self.In_Args["kgd"]

		_d_base = self.data[self._complex]


		v=np.zeros(self._samplesNum+((self._kgd+2)*self._shgd), dtype=np.complex64)
		mas = np.zeros((self._samplesNum, self._kgd ), dtype=np.complex64)
		mas_amp = {} # np.zeros((self._samplesNum, self._kgd ), dtype=np.float32)
		# v = _d_base
		if self._nfgdfu<0:
			v[step:(self._samplesNum+step)] = _d_base
		else:
			v[0:self._samplesNum] = _d_base

		mas_amp = {}
		for i in range(self._kgd):
			j=i*step
			mas[:, i] = v[j: j + nFFt]
			v00 = v[j: j + nFFt]
			_v01 = [np.sqrt(np.pow(v00[i].real, 2) + np.pow(v00[i].imag, 2))  for i in range(len(v00)) ]
			mas_amp[i] = (np.array(_v01), 0)
			# TypePlot.TypePlot.D2

			# hagm =np.abs(fft(v00))
			# # hagm = hagm[:int(len(hagm)/2)]
			# hagm = hagm[:20]
			# mas_amp[i]=(np.array(_v01), hagm)

		self.SubPlots(TypePlot=TypePlot.TypePlot.D1Hor, d =mas_amp)
		# self.spectrum = self.WalshAll(d, nFFt, step)
		k=1