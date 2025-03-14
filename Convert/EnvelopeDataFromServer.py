
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

if __name__ == '__main__':
	''' Конвертируем данные с сервера в формат pandas по AM & FM  '''
	# _path = "/home/alanin/Python/Data/RawData/Servet/AM/"
	# _path =  "/home/alanin/Downloads/DATA-FROM-SERVER/reports/"  		#"/home/alanin/Downloads/DATA-FROM-SERVER/testcases/"
	_path =  "/home/alanin/Downloads/DATA-FROM-SERVER/reports_4_threads/"  		#"/home/alanin/Downloads/DATA-FROM-SERVER/testcases/"
	# _path_conv= "/home/alanin/Python/Data/InputData/TestGPU/amfm01_thread_1.parquet"
	_path_conv= "/home/alanin/Python/Data/InputData/TestGPU/nvideo_01_thread_2.parquet"
	_d_path = {}
	_d_path["amd"]="/home/alanin/Python/Data/InputData/TestGPU/amfm01_thread_1.parquet"
	_d_path["n1"]="/home/alanin/Python/Data/InputData/TestGPU/nvideo_01_thread_1.parquet"
	_d_path["n2"]="/home/alanin/Python/Data/InputData/TestGPU/nvideo_01_thread_2.parquet"
	_d_path["n3"]="/home/alanin/Python/Data/InputData/TestGPU/nvideo_01_thread_3.parquet"
	_d_path["n4"]="/home/alanin/Python/Data/InputData/TestGPU/nvideo_01_thread_4.parquet"

	_server = ServerAMFM()
	# df = _server.find_path_data(_path, AMFM.AM, 'times') #  'reports'   'times'
	# _server.write_pandas_parquet(_path_conv, df)
	_server.load_pandas(_path_conv)
	# _server.load_pandas(_d_path)
	_server.midel_time()

	stop=1