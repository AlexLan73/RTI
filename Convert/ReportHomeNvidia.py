from Convert.Core.ConvertHomeTimeToPandas import HomeTimeToPandas
from Convert.Core.ReadWrite import ReadWrite

def get_path():
	path_base = "/home/alanin/Python/Data/TestGPU/"
	# _path =path_base+"OpenCl_add1.json"
	_path =path_base+"OpenCl_vec_add.json"
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
	""" Данные из json файла
				тест NVidia OpenCL  
	"""
	print('== Тест производительности ==')

	_home_test =  HomeTimeToPandas()
	""" формируем данные в формате pandas  """
	_d_add_1 = _home_test.json_to_pandas(get_path())
	_home_test.calc_forms(get_path_pandas())
	stop=1

