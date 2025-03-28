
import re
#
# import numpy as np
# import matplotlib.pyplot as plt
# import statistics

from Convert.Core.ConvertTo import ConvertTo
from Convert.Core.ReadWrite import ReadWrite
from Convert.Core.ServerAMFM import ServerAMFM
from Core.ServerAMFM import ServerAMFM
from Core.Enum.AMFM import AMFM
import pandas as pd
import pprint

def all_path():
	_d_path = {}
	_d_path["amd"]="/home/alanin/Python/Data/TestGPU/amfm01_thread_1.parquet"
	_d_path["n1"]="/home/alanin/Python/Data/TestGPU/nvidia_01_thread_1.parquet"
	_d_path["n2"]="/home/alanin/Python/Data/TestGPU/nvidia_01_thread_2.parquet"
	_d_path["n3"]="/home/alanin/Python/Data/TestGPU/nvidia_01_thread_3.parquet"
	_d_path["n4"]="/home/alanin/Python/Data/TestGPU/nvidia_01_thread_4.parquet"
	return  _d_path

def one_path():
	''' Конвертируем данные с сервера в формат pandas по AM & FM  '''
	# _path = "/home/alanin/Python/Data/RawData/Servet/AM/"
	# _path =  "/home/alanin/Downloads/DATA-FROM-SERVER/reports/"  		#"/home/alanin/Downloads/DATA-FROM-SERVER/testcases/"
	# _path =  "/home/alanin/Downloads/DATA-FROM-SERVER/reports_4_threads/"  		#"/home/alanin/Downloads/DATA-FROM-SERVER/testcases/"
	# _path_conv= "/home/alanin/Python/Data/TestGPU/amfm01_thread_1.parquet"
	# __path = "/home/alanin/Python/Data/InputData/TestGPU/nvidia_01_thread_1.parquet"
		# __path = "/home/alanin/Python/Data/InputData/TestGPU/Nikola.parquet"
	__path = "Nikola_24_march_2.parquet"
	# __path = "t1_nv_24_march.parquet"

	return __path

if __name__ == '__main__':
	_path = "/home/alanin/Downloads/DATA-FROM-SERVER/24_march/"
	_server = ServerAMFM()
	'''  конвертируем входные данные в формат pamdas   '''
	# df = _server.find_path_data(_path, AMFM.AM, 'times') #  'reports'   'times'
	# df = _server.del_field(df)
	# _server.write_pandas_parquet( one_path(), df)

	'''  грузим данные из с форматом pandas   '''
	# _server.load_pandas(all_path())
	_server.load_pandas(one_path())
	# _server.midel_time()
	# _server.comparison_of_streams()
	# _server.comparison_of_nikolay()
	# _server.ComvertToExcel("Nikola_24_march_2")
	stop=1