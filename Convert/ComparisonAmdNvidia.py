

from Core.NVidia_vs_AMD_comparison import NVidia_vs_AMD_comparison


if __name__ == '__main__':
	""" Сравнение данных ADM и NVidia 	"""
	print('== Тест производительности карт ADM и NVidia ==')
	_test = NVidia_vs_AMD_comparison()
	_test.load_data_AMD_NVIDIA("amfm01_thread_1", "nvidia_01_thread_1")
	k=1