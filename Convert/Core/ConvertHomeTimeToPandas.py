from Convert.Core.ReadWrite import ReadWrite
import pandas as pd


class HomeTimeToPandas(ReadWrite):
	def __init__(self, **kwargs):
		super().__init__()
		self.db = None

	def json_to_pandas(self, path):
		_d = self.load_json(path)
		_fields = list((_d['0'][0]).keys())
		_d0 = {x:[] for x in _fields}

		for key, val in _d.items():
			for key0 in val:
				for key1, val1 in key0.items():
					_d0[key1].append(val1)

		_df = pd.DataFrame(_d0)
		self.write_pandas_parquet("opencl_home_lan_vec_add", _df)

	def calc_forms(self, param):
		_path_df = param[0]
		_name_report = param[1]
		_name_exsal = param[2]
		_df = self.load_pandas_parquet(_path_df)
		unique_field = _df[['n_count', 'count_v', 'size_byte']].drop_duplicates()
		grouped_mean = _df.groupby('n_count')[['total', 'write', 'run', 'read']].mean() #.agg(['mean'])
		grouped_std = _df.groupby('n_count')[['total', 'write', 'run', 'read']].std()  # .agg(['std'])

		new_df_mean = grouped_mean.stack().reset_index()
		new_df_std = grouped_std.stack().reset_index()

		__df =  pd.concat([unique_field, new_df_mean, new_df_std], axis=1)
		self.write_pandas_to_excel(_name_exsal, __df)

	def json_to_pandas_Walera(self, path):
		_d = self.load_json(path)
		v0 = _d[0]
		_key0 = list(v0.keys())
		_key0.remove('gpu_time')
		gpu_key =list( v0['gpu_time'].keys())
		_key01 = _key0 + gpu_key
		_d0 = {x:[] for x in _key01}

		for it in _d:
			for key_00 in _key0:
				if key_00 == 'lang':
					v = it[key_00]
					if v == "OpenCL":
						v="Open_CL"
					_d0[key_00].append(v)
				else:
					_d0[key_00].append(it[key_00])

			for keyx, valx in it['gpu_time'].items():
				_d0[keyx].append(valx)

		_df = pd.DataFrame(_d0)
		self.write_pandas_parquet("opencl_cuda_walera", _df)

	def calc_forms_Walera(self, *args):
		_path_parquet = args[0]
		_path_exsel_add = args[1]
		_path_exsel_vec_sum = args[2]
		_d = self.load_pandas_parquet(_path_parquet)

		v_add = self.calc_df_walera(_d, "add_one")
		v_vector_sum = self.calc_df_walera(_d, "vector_sum")

		self.write_pandas_to_excel(_path_exsel_add, v_add)
		self.write_pandas_to_excel(_path_exsel_vec_sum, v_vector_sum)

		dd=1

	def calc_df_walera(self, df, field):
		_df = df[df["function"]==field]
		_df = _df.drop('function', axis=1)
		_df = _df.reset_index(drop=True)

		_name_row =sorted(df['size'].unique())

		# Добавление столбца 'Senior' по условию
		# vv0 = df[df['size'].unique()]

		# Копирование столбцов 'Name' и 'Salary' в новый DataFrame
		# new_df = vv0[['size', 'mem_size']].copy()
		new_df = df.groupby('size')['mem_size'].first().reset_index()

		df_name_size = pd.DataFrame(_name_row, columns=['Size'])
		df_name_size = df_name_size.astype(int)
		# _dv_lang = _df.sort_values(by='lang')
		_db_cuda = _df[_df['lang']=='CUDA']
		_db_cuda = _db_cuda.reset_index(drop=True)
		_db_cuda = _db_cuda.drop('lang', axis=1)
		d0_cuda = self.form_data_var_std(_db_cuda)
		d0_cuda.columns = [x+"_cuda" for x in d0_cuda.columns.tolist()]
		# d0_cuda = d0_cuda.rename(columns={'cpu_mean': 'cpu_mean_cuda'})
		_db_openCl = _df[_df['lang']=='Open_CL']
		_db_openCl = _db_openCl.reset_index(drop=True)
		_db_openCl = _db_openCl.drop('lang', axis=1)
		d0_openCl = self.form_data_var_std(_db_openCl)
		d0_openCl.columns = [x+"_opencl" for x in d0_openCl.columns.tolist()]
		v0 = pd.concat([new_df, d0_openCl, d0_cuda], axis=1)
		return v0


		# grouped_result = _df.groupby(['lang', 'size']).agg({
		# 	"cpu_clock_total": 'var',
		# 	"run": 'var',
		# 	"read": 'var',
		# 	"total": 'var',
		# 	"write": 'var'
		# })

		# df_opencl1 = df_opencl.drop('lang', axis=1)
		# df_cuda = df_cuda.drop('lang', axis=1)
		#
		# df_opencl2 = df_opencl1.reset_index(drop=True) #  _df[_df["lang"]=='OpenCl']
		# df_cuda = df_cuda.reset_index(drop=True)
		#
		# df_opencl3 = df_opencl2.groupby(['size']).agg({
		# 	"cpu_clock_total": 'var',
		# 	"run": 'var',
		# 	"read": 'var',
		# 	"total": 'var',
		# 	"write": 'var'
		# })

		kk=1

		# grouped_result = _df.groupby(['size', 'lang']).agg({
		# 	"time_total": 'std',
		# 	"time_fft": 'std',
		# 	"time_write": 'std'
		# })

		#var std
		k=1

	def form_data_var_std(self, df0):
		_cpu_clock_mean = df0.groupby('size')['cpu_clock_total'].mean()
		_total_mean = df0.groupby('size')['total'].mean()
		_write_mean = df0.groupby('size')['write'].mean()
		_run_mean = df0.groupby('size')['run'].mean()
		_read_mean = df0.groupby('size')['read'].mean()
		_cpu_clock_std = df0.groupby('size')['cpu_clock_total'].std()
		_total_std = df0.groupby('size')['total'].std()
		_write_std = df0.groupby('size')['write'].std()
		_run_std = df0.groupby('size')['run'].std()
		_read_std = df0.groupby('size')['read'].std()

		v0 =  pd.concat([_cpu_clock_mean, _cpu_clock_std, _total_mean, _total_std,
													_write_mean, _write_std, _run_mean, _run_std, _read_mean, _read_std], axis=1)

		v0.columns = ['cpu_mean', 'cpu_std', 'total_mean', 'total_std', 'write_mean', 'write_std', 'run_mean', 'run_std', 'read_mean', 'read_std']
		v0 = v0.reset_index(drop=True)
		return v0
