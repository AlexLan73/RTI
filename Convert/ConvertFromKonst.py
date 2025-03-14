from Convert.Core.ConvertKonstData import ConvertKonst


def get_path_AM():
	_path_dirAF_in = "/home/alanin/Python/Data/RawData/AM_sign2/"  # "/home/alanin/Python/Data/RawData/AM_sign2/"    //home/alanin/Python/Data/RawData/Am_fg2/
	_path_dirAF_out = "/home/alanin/Python/Data/InputData/AM/"
	return _path_dirAF_in, _path_dirAF_out, 1

def get_path_FM():
	_path_dirAF_in = "/home/alanin/Python/Data/RawData/FM GPU 2/"  # /home/alanin/Python/Data/RawData/FM GPU 2/    /home/alanin/Python/Data/RawData/fm/
	_path_dirAF_out = "/home/alanin/Python/Data/InputData/FM/"
	return _path_dirAF_in, _path_dirAF_out, 0

if __name__ == '__main__':
    print('== Convert ==')
    _conver = ConvertKonst(get_path_FM())
    _conver.convert_standart()
    k1 = 1