
import pandas as pd
from functools import wraps

def drop_columns_decorator(columns_to_drop):
    """Декоратор для удаления указанных столбцов из DataFrame."""
    def decorator(func):
        @wraps(func)
        def wrapper(self, df, *args, **kwargs):
            result = func(self, df, *args, **kwargs)
            return result.drop(columns_to_drop, axis=1, errors='ignore')
        return wrapper
    return decorator

class ComparisonData:
	def __init__(self):
		pass

	@drop_columns_decorator(["report_path", "true_nihs", "nfgd_fu", "sum_samples",
													 'time_sine', 'time_end', 'time_start', "n1grs", "is_am"])
	def del_field_is_am(self, df):
		# Код обработки DataFrame
		return df

	@drop_columns_decorator(["report_path", "true_nihs", "nfgd_fu", "sum_samples",
													 'time_sine', 'time_end', 'time_start', "n1grs"])
	def del_field(self, df):
		# Код обработки DataFrame
		return df

	@drop_columns_decorator(["report_path", 'nl', 'kgrs', 'kgd', 'shgd', 'samples_num',
													 "true_nihs", "nfgd_fu", "sum_samples", 'time_sine', 'time_end',
													 'time_start', "n1grs", "is_am"])
	def del_field_all(self, df):
		# Код обработки DataFrame
		return df

	@drop_columns_decorator(["report_path", "N", 'nl', 'kgd', 'shgd', 'samples_num',
													 "true_nihs", "nfgd_fu", "sum_samples", 'time_sine', 'time_end',
													 'time_start', "n1grs", "is_am"])
	def del_field_N_sum_samples(self, df):
		# Код обработки DataFrame
		return df

	@drop_columns_decorator(['index', 'kgrs'])
	def del_field_kgrs(self, df):
		# Код обработки DataFrame
		return df

	def form_data_var_std(self, df0):
		df0.columns = [str(x).split("_")[1] if "time_" in x else x for x in df0.columns]
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

	def form_data_var_std_ls(self, df0, ls):
		df0.columns = [str(x).split("_")[1] if "time_" in x else x for x in df0.columns]
		_total_mean = df0.groupby(ls)['total'].mean()
		_total_std = df0.groupby(ls)['total'].std()
		_write_mean = df0.groupby(ls)['write'].mean()
		_write_std = df0.groupby(ls)['write'].std()
		_run_mean = df0.groupby(ls)['fft'].mean()
		_run_std = df0.groupby(ls)['fft'].std()
		_read_mean = df0.groupby(ls)['read'].mean()
		_read_std = df0.groupby(ls)['read'].std()
		v0 =  pd.concat([_total_mean, _total_std,_write_mean, _write_std, _run_mean, _run_std, _read_mean, _read_std], axis=1)
		v0.columns = ['total_mean', 'total_std', 'write_mean', 'write_std', 'fft_mean', 'fft_std', 'read_mean', 'read_std']
		v0 = v0.reset_index(drop=True)
		return v0