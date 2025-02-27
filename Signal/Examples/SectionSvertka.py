import numpy as np
from scipy.signal import fftconvolve


def sectioned_convolve(long_signal, short_signal, section_size=2 ** 13):
	"""
	Вычисляет секционную свертку длинного сигнала с коротким сигналом.

	:param long_signal: Длинный сигнал.
	:param short_signal: Короткий сигнал.
	:param section_size: Размер секции.
	:return: Результат свертки.
	"""
	# Инициализация результата
	result = np.zeros(len(long_signal) + len(short_signal) - 1)

	# Разбиение длинного сигнала на секции
	for i in range(0, len(long_signal), section_size):
		section = long_signal[i:i + section_size]

		# Вычисление свертки секции с коротким сигналом
		section_conv = fftconvolve(section, short_signal, mode='full')

		# Суммирование результата в общий массив
		start_idx = i
		end_idx = start_idx + len(section_conv)
		result[start_idx:end_idx] += section_conv

	return result


# Пример использования
if __name__ == "__main__":
	# Генерация сигналов для примера
	long_signal = np.random.rand(2 ** 16)  # Длинный сигнал
	short_signal = np.random.rand(2 ** 16)  # Короткий сигнал

	# Вычисление секционной свертки
	result = sectioned_convolve(long_signal, short_signal)

	print("Результат секционной свертки:", result.shape)
