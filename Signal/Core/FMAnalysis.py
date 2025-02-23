import asyncio

import numpy as np
import json
from AMFM import AMFM
from PlotOne import PlotInfoOne
from SignalBase0 import SignalBase0, ConvertToComplex
from TypePlot import TypePlot

class FMAnalysis(SignalBase0):
	def __init__(self, **kwargs):
		super().__init__(AMFM.FM)
		print("__ Анализируем ФМ сигнал __")
		self._input_dir_base = "/home/alanin/Python/Data/OUT/FM/"
		self._dir_data = "000"
		self._in_args = "in_args.json"
		self._name_tfpMSeqSigns = "tfpMSeqSigns.json"
		self._out_json = "out.json"
		self._ftps_args = "ftps.json"
		self.__ParserArg(**kwargs)


	def __ParserArg(self, **kwargs):
		self._input_dir_base =  kwargs.get("InputDirDataBase", self._input_dir_base )
		self._dir_data =  kwargs.get("DirData", self._dir_data)
		self._path_works_data = self._input_dir_base+self._dir_data


	def set_params_strob(self, **kwargs):
		self.__ParserArg(**kwargs)


	def run(self):
		self.load_json(self._path_works_data)
		_d = self._dataOut["polar0"].Am
		# self.GraphPlot(d=_d, TypePlot=TypePlot.D1Hor, xNL=2,  show="show")
		# self.GraphAndFFTPosledPlot()	#  крылья
		# self.GraphAndFFTPlot(d=_d, xNL=2,  show="show")
		self.SpectrumAnd(d=_d)  # расчет FM
		# self.SignalAndOporaFFTPlot(d=_d)
		k=1

	def GraphAndFFTPosledPlot(self):
		self._show = "show"
		self._typePlot = TypePlot.D2
		_d = {}
		_fft =  self.FFTMSeqSignsAm
		# _fft = _fft[:int(len(_fft)//2)]
		_d[0]= (PlotInfoOne(x=self._tfpMSeqSigns), PlotInfoOne(x=_fft, Title="spectrum"))
		super().SubPlots(d=_d)

	def SpectrumAnd(self, **kwargs):
		self._typePlot = TypePlot.D1Vert
		self._show = "show"
		self.ParserArg(**kwargs)
		_countD = len(self._data)
		_nl = self.Params["NL"]
		_kgd = self.Params["kgd"]
		_d = {}
		_l = self.Params["samplesNum"]
		# """ получим значения одного луча """
		_dx = np.array(self._data[0:_l])  # считывается все значение по лучу
		_dx = _dx[0: self._countPosled]   # приводится к размерности БПФ
		spectrum_inData = np.fft.fft(_dx)

		n1grs = self.Params["n1grs"]
		ind0 = int(round(n1grs * self.C,0)) % self._countPosled
		# _fft_tfpMSeq_base = np.fft.fft(self._tfpMSeqSigns)
		# _fft_MSeqBase = np.concatenate((_fft_tfpMSeq_base[ind0:] , _fft_tfpMSeq_base))
		# _fft_end = _fft_tfpMSeq_base[:ind0]
		# _fft_MSeqBase = np.concatenate((_fft_MSeqBase, _fft_end))
		lsData =[]
		# _dv={}
		_dvN={}
		log2N = np.uint32(np.log2(self._countPosled))
		# for v in range(self.Params["kgrs"]):
		_kv = 0
		for v in range(1):
			print(f" kgrs-> {v} ")
			# indxxC = int(round((v + n1grs) * self.C, 0)) % self._countPosled
			# if n1grs+v < 0:
			# 	_fft_begin  =_fft_tfpMSeq_base[indxxC:]
			# 	_fft_maska = np.concatenate((_fft_begin, _fft_tfpMSeq_base))
			# else:
			# 	_fft_end  =_fft_tfpMSeq_base[:indxxC]
			# 	_fft_maska = np.concatenate((_fft_tfpMSeq_base, _fft_end))
			# _fft_maska = _fft_maska[:self._countPosled]

			# if len(_fft_maska) != len(spectrum_inData):
			# 	dddd=1
			_v = np.abs(np.fft.ifft(spectrum_inData * self.FFTMSeqSigns))
			# _v = np.abs(np.fft.ifft(spectrum_inData * _fft_maska))
			# _lsInd = [self.rbs( np.uint32(i), log2N) for i in range(self._countPosled)]
			# __d = [_v[self.rbs( np.uint32(i), log2N)] for i in range(self._countPosled)]
			# _conpl = [__d[i] for i in range(_kgd)]
			_conpl = [_v[i] for i in range(_kgd)]
			# _amp = np.abs(_conpl)
			_amp = _v
			# _amp =np.abs( [z.real for z in _conpl])
			_d[_kv] = (PlotInfoOne(x=_amp), 0,)
			_kv=_kv + 1
			# _d[v] = (PlotInfoOne(x=_amp, Title=f" signal {v} "), 0,)
			stop=1

		super().SubPlots(d=_d)
		return

		self._xNl = 2
		for it in range(self._xNl):   #self._xNl
			i = it * _l
			_dx = np.array(self._data[i:min(i + _l, _countD)])
			_dx = _dx[0: self._countPosled]

			spectrum1 = np.fft.fft(_dx)
			spectrum2 = np.fft.fft(self._tfpMSeqSigns)
			result_spectrum = spectrum1 * spectrum2
			# Применяем обратное БПФ для получения результата
			result_signal = np.fft.ifft(result_spectrum)
			result_signal =np.abs(result_signal)
			# _fft =  np.abs(scipy.fft.fft(_dx))
			# _fftAnd = _fft * self.FFTMSeqSignsAm
			_fftAnd = np.abs(result_spectrum)
			# _fft = _fft[:int(len(_fft)//2)]
			# _d[it]= (PlotInfoOne(x=_fft, Title=" basa spectrums "), PlotInfoOne(x=_fftAnd, Title=" & spectrums "))

			_d[it]= (PlotInfoOne(x=_fftAnd, Title=" & spectrums "), PlotInfoOne(x=result_signal, Title=" IFFT "), )

		super().SubPlots(d=_d)
		stopp =1


