from Convert.Core.ConvertToComplex import ConvertToComplex
from Signal.Core.FFTone import FFTone
from Graphs.Core.PlotOne import PlotOne, PlotInfoOne
from threading import Thread
from time import sleep, perf_counter
import time
from Core.Enum.AMFM import AMFM
import numpy as np
import math
import asyncio
import json
import cmath # Для работы с комплексными числами
import math  # Для работы с math.hypot
import Core.Enum.TypePlot
from scipy.fft import fft, ifft
import scipy.fft


#
# class DataOut:
# 	def __init__(self):
# 		self.Re = None
# 		self.Im = None
# 		self.Complex = None
# 		self.Am = None
#
#
# class ConvertToComplex:
# 	def __init__(self, d=None):
# 		if not(d is None):
# 			self.split_complex_list(d)
#
# 	def split_complex_list(self, data):
# 			"""
# 			Преобразует список кортежей (int, int) в отдельные списки:
# 			- Комплексные числа
# 			- Вещественные числа
# 			- Мнимые числа
# 			- Огибающая (модуль комплексного числа)
# 			"""
# 			d = DataOut()
# 			d.Complex  = list(map(lambda x: complex(x[0], x[1]), data))
# 			d.Re = list(map(lambda x: x.real, d.Complex))
# 			d.Im = list(map(lambda x: x.imag, d.Complex))
# 			d.Am = list(map(lambda x: math.hypot(x.real, x.imag), d.Complex))
# 			return d
#
# 	def split_Am(self, data):
# 			d = DataOut()
# 			d.Complex  = list(map(lambda x: complex(x[0], x[1]), data))
# 			d.Am = list(map(lambda x: math.hypot(x.real, x.imag), d.Complex))
# 			return d
#
# 	def split_Re(self, data):
# 			d = DataOut()
# 			d.Complex  = list(map(lambda x: complex(x[0], 0), data))
# 			d.Re = list(map(lambda x: x.real, d.Complex))
# 			d.Am = d.Re
# 			return d


class SignalBase0(PlotOne, FFTone):
	def __init__(self, amfm: AMFM):
		PlotOne.__init__(self)
		FFTone.__init__(self)
		self.FFTMSeqSignsAm = None
		self._tfpMSeqSigns = None
		self._dataOut = {} #DataOut()
		self.Params = None
		self.typeSignal = amfm
		self._path_works = ""
		self._dir_data = "000"
		self._in_args = "in_args.json"
		self._name_tfpMSeqSigns = "tfpMSeqSigns.json"
		self._out_json = "out.json"
		self._ftps_args = "ftps.json"
		self._count2N = 0
		self.FFTMSeqSigns = None
		self._Dftps = {}
		self._xNl = 1
		self.C = 0
		self._input_dir_base =""

	def _ParserArg(self, **kwargs):
		self._input_dir_base =  kwargs.get("InputDirDataBase", self._input_dir_base )
		self._dir_data =  kwargs.get("DirData", self._dir_data)
		self._path_works_data = self._input_dir_base+self._dir_data


	def TaskLoadOut(self, path:str, amfm: AMFM):
		start_time = time.time()
		# await asyncio.sleep(0)
		print(f" Load Out-> {path} ")
		_path_file = self._path_works + "/" + self._out_json
		with open(_path_file, "r") as file:
				_out = json.load(file)

		if _out is None:
			raise f"Error in TaskLoadOut problem in _out = json.load(file)-> {_path_file} "

		_comvert = ConvertToComplex()
		for key, val in _out.items():
			self._dataOut[key] = _comvert.split_Re(val) if amfm==AMFM.FM else  _comvert.split_complex_list(val)

		end_time = time.time()
		execution_time = end_time - start_time
		print(f"Out-> {path} Время выполнения: {execution_time} секунд")

	def TaskLoadtfpMSeqSigns(self, path:str, amfm: AMFM):
		start_time = time.time()
		print(f" Load MSeqSigns-> {path} ")

		if amfm == AMFM.FM:
			with open(self._path_works + "/" + self._name_tfpMSeqSigns, 'r') as file:
				self._tfpMSeqSigns = json.load(file)
			self._countPosled = len(self._tfpMSeqSigns)
			self._count2N = 2 ** math.ceil(math.log2(self._countPosled))
			self._tfpMSeqSigns = self._tfpMSeqSigns + [0] * (self._count2N - self._countPosled)
			x = np.array(self._tfpMSeqSigns)
			# Compute FFT and its inverse
			self.FFTMSeqSigns =  fft(x)
			self.FFTMSeqSignsAm = np.abs(fft(x))
		end_time = time.time()
		execution_time = end_time - start_time
		print(f"MSeqSigns-> {path} Время выполнения: {execution_time} секунд")

	def TaskLoadftps(self, path, amfm: AMFM):
		start_time = time.time()
		print(f" Load ftps-> {path} ")

		path_file = self._path_works + "/" + self._ftps_args
		with open(path_file, "r") as file:
				_out = json.load(file)

		_comvert = ConvertToComplex()
		for key, val in _out.items():
			self._Dftps[key] = _comvert.split_Am(val)
			k=key
			v=val

		end_time = time.time()
		execution_time = end_time - start_time
		print(f"ftps-> {path} Время выполнения: {execution_time} секунд")

	def load_json(self, path_works):
		self._path_works = path_works

		threads = []
		_taskLoadftps = Thread(target=self.TaskLoadftps, args=(path_works, self.typeSignal,))
		threads.append(_taskLoadftps)
		_taskLoadftps.start()
		_taskLoadOut = Thread(target=self.TaskLoadOut, args=(path_works, self.typeSignal,))
		threads.append(_taskLoadOut)
		_taskLoadOut.start()
		_taskLoadtfpMSeqSigns = Thread(target=self.TaskLoadtfpMSeqSigns, args=(path_works, self.typeSignal,))
		threads.append(_taskLoadtfpMSeqSigns)
		_taskLoadtfpMSeqSigns.start()

		with open(self._path_works + "/" + self._in_args, 'r') as file:
			self.Params = json.load(file)
			self.Params["NL"] = self.Params["nl"]
			self.Params["trueNihs"] = self.Params['true_nihs']
			self.Params["nfgdfu"] = self.Params['nfgd_fu']
			self.Params["samplesNum"] = self.Params['samples_num']
			k=1

		for t in threads:
			t.join()

		if self.Params is not None:
			self.C = self.Params["samplesNum"]/2/(self.Params["trueNihs"]+2)
		print("***    загрузили    ***")

	def ParserArg(self, **kwargs):
		self._xNl = kwargs.get("xNL", self.Params["NL"])
		super().ParserArg(**kwargs)

	def GraphPlot(self, **kwargs):
		self.ParserArg(**kwargs)
		_countD = len(self._data)
		_nl = self.Params["NL"]
		_d = {}
		_l = self.Params["samplesNum"]
		for it in range(self._xNl):
			i=it*_l
			_dx = np.array(self._data[i:min(i+_l,_countD)])
			_d[it]= (PlotInfoOne(x=_dx, nameX=str(f"Time  {it}" ),  nameY=str(f"Ampl  {it}" ), Title=str(f" graph - {it}")),0)

		super().SubPlots(d=_d)
		stopp =1

	def rbs(self, x: np.uint32, log2N: np.uint32):
		x = (((x & 0xaaaaaaaa) >> 1) | ((x & 0x55555555) << 1))
		x = (((x & 0xcccccccc) >> 2) | ((x & 0x33333333) << 2))
		x = (((x & 0xf0f0f0f0) >> 4) | ((x & 0x0f0f0f0f) << 4))
		x = (((x & 0xff00ff00) >> 8) | ((x & 0x00ff00ff) << 8))
		x = ((x >> 16) | (x << 16))
		x = x >> (32 - log2N)
		return x

	def GraphAndFFTPlot(self, **kwargs):
		self._typePlot = TypePlot.D2
		self.ParserArg(**kwargs)
		_countD = len(self._data)

		_nl = self.Params["NL"]
		_d = {}
		_l = self.Params["samplesNum"]

		for it in range(self._xNl):
			i=it*_l
			i = it * _l
			_dx = np.array(self._data[i:min(i + _l, _countD)])
			_fft =  np.abs(scipy.fft.fft(_dx))
			# _fft = _fft[:int(len(_fft)//2)]
			_d[it]= (PlotInfoOne(x=_dx), PlotInfoOne(x=_fft, Title="spectrum"))

		super().SubPlots(d=_d)
		stopp =1

	def SignalAndOporaFFTPlot(self, **kwargs):
		self._typePlot = TypePlot.D2
		self._show = "show"
		self.ParserArg(**kwargs)
		_countD = len(self._data)

		_nl = self.Params["NL"]
		_d = {}
		_l = self.Params["samplesNum"]

		_dx = np.array(self._data[0:self._countPosled])
		_fft = np.abs(scipy.fft.fft(_dx))
		# _d[0] = (PlotInfoOne(x=_dx), PlotInfoOne(x=_fft, Title="spectrum"))

		_fft_sig =  self.FFTMSeqSignsAm
		# _fft = _fft[:int(len(_fft)//2)]
		# _d[1]= (PlotInfoOne(x=self._tfpMSeqSigns), PlotInfoOne(x=_fft_sig, Title="spectrum"))

		_fft_and = _fft * _fft_sig
		_ifft = np.abs(np.fft.ifft(_fft_and))
		_d[0] = (PlotInfoOne(x=_ifft), PlotInfoOne(x=_fft_and, Title="spectrum"))

		super().SubPlots(d=_d)
		stopp =1
