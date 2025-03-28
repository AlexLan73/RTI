from Convert.Core.ReadWrite import ReadWrite
import pandas as pd


class NVidia_vs_AMD_comparison(ReadWrite):
	def __init__(self):
		super().__init__()
		self._path_dir_test_gpu = "/home/alanin/Python/Data/TestGPU/"
		# self._path_amd =""
		# self._path_nvidia = ""
		self._df_amf = None
		self._df_nvidia = None

	def load_data_AMD_NVIDIA(self, *args):
		_path_amd = args[0]
		_path_nvidia = args[1]
		_df_adm = self.load_pandas_parquet(_path_amd)
		_df_nvidia =  self.load_pandas_parquet(_path_nvidia)

		# columns_to_drop = ['time_sine', 'time_start', 'time_end']  #
		# ["N", "nl", "n1grs", "kgrs","kgd", "shgd", "samples_num",
		#  "is_am", "sum_samples", "time_total", "time_sine", "time_start", "time_end"]

		columns_to_drop = ["report_path", "true_nihs", "nfgd_fu", "sum_samples",
											 'time_sine', 'time_end', 'time_start', "n1grs"]  # 'time_start',

		_df_adm = _df_adm.drop(columns_to_drop, axis=1)
		_df_adm = _df_adm[_df_adm["is_am"]==0]
		_df_nvidia = _df_nvidia.drop(columns_to_drop, axis=1)
		_nvidia_n = _df_nvidia[(_df_nvidia["is_am"]==0) & (_df_nvidia["time_total"]>0.0)]["N"]
		_ls_n =list(_nvidia_n.unique())

		_df_nvidia = (_df_nvidia.loc[_df_nvidia['N'].isin(_ls_n)]).drop('is_am', axis=1)
		_df_adm = (_df_adm.loc[_df_adm['N'].isin(_ls_n)]).drop('is_am', axis=1)
		_df_adm.columns = [str(x).split("_")[1] if "time_" in x else x for x in _df_adm.columns]
		_df_nvidia.columns = [str(x).split("_")[1] if "time_" in x else x for x in _df_nvidia.columns]

		new_df = _df_nvidia.groupby('N')[['nl', 'kgrs', "kgd", "samples_num"] ].first().reset_index()

		columns_to_drop = ["nl", "kgrs","kgd", "shgd", "samples_num"]
		_df_adm = _df_adm.drop(columns_to_drop, axis=1)
		_df_nvidia = _df_nvidia.drop(columns_to_drop, axis=1)
		_df_adm = self.form_data_var_std(_df_adm)
		_df_adm.columns = ["amd_"+x for x in _df_adm.columns]
		_df_nvidia = self.form_data_var_std(_df_nvidia)
		_df_nvidia.columns = ["nvidia_"+x for x in _df_nvidia.columns]
		_df_basa =  pd.concat([new_df, _df_adm, _df_nvidia], axis=1)
		_df_sort = _df_basa.sort_values(by='amd_total_mean')

		self.write_pandas_to_excel("Compari_amd_nvidia", _df_basa)
		self.write_pandas_to_excel("Compari_amd_nvidia_sort", _df_sort)

	def form_data_var_std(self, df0):
		_total_mean = df0.groupby('N')['total'].mean()
		_total_std = df0.groupby('N')['total'].std()
		_write_mean = df0.groupby('N')['write'].mean()
		_write_std = df0.groupby('N')['write'].std()
		_run_mean = df0.groupby('N')['fft'].mean()
		_run_std = df0.groupby('N')['fft'].std()
		_read_mean = df0.groupby('N')['read'].mean()
		_read_std = df0.groupby('N')['read'].std()
		v0 =  pd.concat([_total_mean, _total_std,_write_mean, _write_std, _run_mean, _run_std, _read_mean, _read_std], axis=1)
		v0.columns = ['total_mean', 'total_std', 'write_mean', 'write_std', 'fft_mean', 'fft_std', 'read_mean', 'read_std']
		v0 = v0.reset_index(drop=True)
		return v0
