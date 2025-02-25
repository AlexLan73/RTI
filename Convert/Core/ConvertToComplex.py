from Convert.Core.DataOut import DataOut

import math  # Для работы с math.hypot


class ConvertToComplex:
	def __init__(self, d=None):
		if not(d is None):
			self.split_complex_list(d)

	def split_complex_list(self, data):
			"""
			Преобразует список кортежей (int, int) в отдельные списки:
			- Комплексные числа
			- Вещественные числа
			- Мнимые числа
			- Огибающая (модуль комплексного числа)
			"""
			d = DataOut()
			d.Complex  = list(map(lambda x: complex(x[0], x[1]), data))
			d.Re = list(map(lambda x: x.real, d.Complex))
			d.Im = list(map(lambda x: x.imag, d.Complex))
			d.Am = list(map(lambda x: math.hypot(x.real, x.imag), d.Complex))
			return d

	def split_Am(self, data):
			d = DataOut()
			d.Complex  = list(map(lambda x: complex(x[0], x[1]), data))
			d.Am = list(map(lambda x: math.hypot(x.real, x.imag), d.Complex))
			return d

	def split_Re(self, data):
			d = DataOut()
			d.Complex  = list(map(lambda x: complex(x[0], 0), data))
			d.Re = list(map(lambda x: x.real, d.Complex))
			d.Am = d.Re
			return d
