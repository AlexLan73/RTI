
import re
from Convert.Core.ReadWrite import ReadWrite


class ConvertTo(ReadWrite):
	def __init__(self):
		super().__init__()
		pass

	def txt_test_gpu0(self, path):
		lines = self.load_txt_line(path)
		# with open(path, 'r') as file:
		# 	lines = file.readlines()
		k = 0
		_d = {}
		numbers = []
		for it in range(1, len(lines)):
			# Удаляем перевод строки
			line = str(lines[it]).replace("'","").strip()
			_lineS = re.sub(r'\s+', ' ', line).split(" ")
			_d_info = {}
			_d_info["file"] = _lineS[0]
			_d_info["samples"] = int(_lineS[4])
			_d_info["time_full"] = float(_lineS[7])
			_d_info["time_fft"] = float(_lineS[8])
			_d[k] = _d_info
			k += 1

		data = {}
		_d_time = [(val["samples"], val["time_full"], val["time_fft"]) for val in _d.values()]
		_xsamp = [x[0] for x in _d_time]
		_full = [x[1] for x in _d_time]
		_fft = [x[2] for x in _d_time]
		data["xsamp"]=_xsamp
		data["full"] = _full
		data["fft"] = _fft
		return data
