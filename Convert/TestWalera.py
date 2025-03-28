
from Convert.Core.ConvertHomeTimeToPandas import HomeTimeToPandas
from Convert.Core.ReadWrite import ReadWrite

def get_path():
	path_base = "/home/alanin/Python/Data/TestGPU/"
	_path =path_base+"report_2025-03-17_13:38:35.json"
	return _path

def get_path_pandas():
	_name_path = ("opencl_home_lan_vec_add.parquet",
								"NVidia тест на OpenCL, в сумма вестора ",
								"OpenCL_home_vector_sum")

	# _name_path = ("opencl_home_lan_add1",
	# 							"NVidia тест на OpenCL, в значение вестора добавить 1 ",
	# 							"OpenCL_home_add1")
	return _name_path


if __name__ == '__main__':
	""" Данные из json файла делал Валера
				тест NVidia OpenCL  и  CUDA
	"""
	print('== Тест скорости выполнения ==')

	_home_test =  HomeTimeToPandas()
	""" формируем данные в формате pandas  """
	# _d_add_1 = _home_test.json_to_pandas_Walera(get_path())
	_home_test.calc_forms_Walera("opencl_cuda_walera", "Walera_add", "Walera_vec_sum")
	stop=1

