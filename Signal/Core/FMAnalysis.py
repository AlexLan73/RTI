import asyncio

import numpy as np
import json
from Core.Enum.AMFM import AMFM
from Graphs.Core.PlotOne import PlotInfoOne
from Signal.Core.SignalBase0 import SignalBase0
from Convert.Core import ConvertToComplex
from Core.Enum.TypePlot import TypePlot
from scipy.fft import fft, ifft
from Core.Enum.TypePlot import TypePlot
import scipy.fft
from scipy import signal
from scipy.signal import fftconvolve


class FMAnalysis(SignalBase0):
	def __init__(self, **kwargs):
		super().__init__(AMFM.FM)
		print("__ Анализируем ФМ сигнал __")
		self._input_dir_base = "/home/alanin/Python/Data/OUT/FM/"
		# self._dir_data = "000"
		# self._in_args = "in_args.json"
		self._name_tfpMSeqSigns = "tfpMSeqSigns.json"
		# self._out_json = "out.json"
		# self._ftps_args = "ftps.json"
		self._ParserArg(**kwargs)

	def set_params_strob(self, **kwargs):
		self._ParserArg(**kwargs)

	def run(self):
		self.load_json(self._path_works_data)
		_d = self._dataOut["polar0"].Am
		# self.GraphPlot(d=_d, TypePlot=TypePlot.D1Hor, xNL=2,  show="show")
		# self.GraphAndFFTPosledPlot()	#  крылья
		# self.GraphAndFFTPlot(d=_d, xNL=2,  show="show")
		# self.SpectrumAnd_W0(d=_d)
		# self.SignalAndOporaFFTPlot(d=_d)
		# self.SpectrumAnd(d=_d)  # расчет FM
		self.CiklSwertka(d=_d)
		k=1

	def GraphAndFFTPosledPlot(self):
		self._show = "show"
		self._typePlot = TypePlot.D2
		_d = {}
		_fft =  self.FFTMSeqSignsAm
		# _fft = _fft[:int(len(_fft)//2)]
		_d[0]= (PlotInfoOne(x=self._tfpMSeqSigns), PlotInfoOne(x=_fft, Title="spectrum"))
		super().SubPlots(d=_d)

	def SpectrumAnd_W0(self, **kwargs):
		""" Свертка опоры и согнала на основной частоте (от 0 отчета) """
		self._typePlot = TypePlot.D2
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
		# _fft_dx0 = scipy.fft.fft(_dx)
		_fft_dx = scipy.fft.fft(_dx)
		_d[0]= (PlotInfoOne(x=_dx), PlotInfoOne(x=_fft_dx, Title="signal"))
		_d[1] = (PlotInfoOne(x=self._tfpMSeqSigns), PlotInfoOne(x= np.abs(self.FFTMSeqSigns), Title="опора"))
		_fft_and =np.abs(_fft_dx*self.FFTMSeqSigns)
		plot1 = np.abs(np.fft.ifft(_fft_and))
		_d[2] = (PlotInfoOne(x=plot1), PlotInfoOne(x=_fft_and, Title="spectrum"))
		super().SubPlots(d=_d)
		return

	def SpectrumAnd(self, **kwargs):
		self._typePlot = TypePlot.D2
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
		# _fft_dx0 = scipy.fft.fft(_dx)
		# _fft_dx = np.abs(scipy.fft.fft(_dx))
		_fft_dx = scipy.fft.fft(_dx)
		n1grs = self.Params["n1grs"]
		kgrs = self.Params["kgrs"]
		for v in range(8):
			# v0 = n1grs * 25000 + v * 21570
			v0 = n1grs+v
			if v0 < 0:
				_fft_begin  =self.FFTMSeqSigns[ self._countPosled-abs(v0):]
				_fft_maska = np.concatenate((_fft_begin, self.FFTMSeqSigns))
				_fft_maska = _fft_maska[:self._countPosled]

			else:
				_fft_end  =self.FFTMSeqSigns[:v0]
				_fft_maska = np.concatenate((self.FFTMSeqSigns, _fft_end))
				_fft_maska = _fft_maska[v0:]

			_dd =np.abs(_fft_dx *_fft_maska)
			_dd[0]=0
			# _dd =np.abs(self.FFTMSeqSigns *_fft_maska)
			# _sigal_0 =np.abs(np.fft.ifft((_fft_dx*_fft_maska)))
			_sigal_0 =np.abs(np.fft.ifft(_dd))
			_kgd=400
			# nfgd_fu = self.Params["nfgd_fu"]
			# if nfgd_fu < 0:
			# 	_sigal = _sigal_0[self._countPosled- abs(nfgd_fu):]
			# 	_sigal = np.concatenate((_sigal, _sigal_0[:_kgd]))
			# 	_sigal = _sigal[:_kgd]
			# else:
			# 	_sigal = _sigal_0[nfgd_fu:nfgd_fu+_kgd]

			# _sigal = np.concatenate((_fft_begin, _sigal_0))

			_d[v]= (PlotInfoOne(x=_sigal_0), PlotInfoOne(x= _dd)) #  _fft_maska
		super().SubPlots(d=_d)
		return

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

	def CiklSwertka(self, **kwargs):
		self._typePlot = TypePlot.D2
		self._show = "show"
		self.ParserArg(**kwargs)
		_countD = len(self._data)
		_nl = self.Params["NL"]
		_kgd = self.Params["kgd"]
		_d = {}
		_l = self.Params["samplesNum"]
		_d = self._tfpMSeqSigns
		_xx =  self._tfpMSeqSigns
		nn=150000
		_xEnd = _xx[len(_xx)-nn:]
		_x0 = np.concatenate((_xEnd, _xx))
		_x0 = _x0[:len(self._tfpMSeqSigns)]
		cyclic_convolution = np.abs(signal.fftconvolve(self._tfpMSeqSigns, self._tfpMSeqSigns, mode='full')) # full valid same
		# cyclic_convolution = np.abs(signal.fftconvolve(_x0, self._tfpMSeqSigns, mode='full')) # full valid same
		# Обрезаем результат, чтобы он соответствовал размеру исходных данных
		cyclic_convolution = cyclic_convolution[len(self._tfpMSeqSigns)-1:len(self._tfpMSeqSigns)+len(self._tfpMSeqSigns)-1]
		_fft =  np.abs(scipy.fft.fft(cyclic_convolution))

		self.OnePlotx(cyclic_convolution)
		self.OnePlotx(_fft)  #, show="show"


