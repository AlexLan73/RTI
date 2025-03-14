import os
import os.path
import pickle

import numpy as np
import json
import re
from pathlib import Path

from sympy import python


class OneBlockDataJson:
  def __init__(self, path_out):
    self._path = path_out
    self.in_args_json = {}
    self.in_args = "in_args.json"
    self.name_tfpMSeqSigns = "tfpMSeqSigns.json"
    self.tfpMSeqSigns={}
    self.out = {}
    self.ftps = {}
    self.id = 0

  def Save(self):
    s = "000" + str(self.id)
    s = s[len(s)-3:]
    self._path =self._path  +s
    print(f" !!!   Save data to -> {self._path}   !!!")
    if not os.path.isdir(self._path):
      os.makedirs(self._path)

    with open(self._path+"/in_args.json", 'w') as file:
      json.dump(self.in_args_json, file)

    print("     save data to -> tfpMSeqSigns  ")
    with open(self._path+"/"+self.name_tfpMSeqSigns, 'w') as file:
      json.dump(self.tfpMSeqSigns, file)

    print("     save data to -> out  ")
    with open(self._path+"/out.json", 'w') as file:
      json.dump(self.out, file)

    print("     save data to -> ftps  ")
    with open(self._path+"/ftps.json", 'w') as file:
      json.dump(self.ftps, file)

    kk=1

class ConvertKonst:
  def __init__(self, *args):
    self._path_input = args[0][0]
    self._path_output = args[0][1]
    self._is_am = args[0][2]
    self._path=""
    self.DSignal = {}
    self._complex = "complex"
    self._in_args = "in_args.json"

    self._ls_in_args =[]
    k=1

  def Load(self, path:str, name_picle):
    if not os.path.exists(path):
      return None
    self._path = path
    file_list =[x for  x in os.listdir(self._path ) if "tfpPreNormalization" in x]

    # 'tfpPreNormalizationRay0Polar1'
    for it in file_list:
      # self._one_file(self._path + "\\" + it, it.replace("tfpPreNormalization", ""))
      self._one_file(self._path  +it, it.replace("tfpPreNormalization", ""))

    if self.DSignal.__len__()>0:
      with open(name_picle+"/data.pickle", 'wb') as f:
        pickle.dump(self.DSignal, f)

    return self.DSignal

  def LoadNew(self, path:str, name_picle):
    if not os.path.exists(path):
      return None
    self._path = path
    file_list =[x for  x in os.listdir(self._path ) if "out" in x]

    # 'tfpPreNormalizationRay0Polar1'
    for it in file_list:
      # self._one_file(self._path + "\\" + it, it.replace("tfpPreNormalization", ""))
      self._one_file_new(self._path  +it)

    if self.DSignal.__len__()>0:
      with open(name_picle+"/data.pickle", 'wb') as f:
        pickle.dump(self.DSignal, f)

    return self.DSignal

  def LoadNew01(self, dd:dict):
    path = dd["path_dir"]
    name_picle = dd["path_file_pickle"]
    path_filter = dd["path_filter"]


    if not os.path.exists(path):
      return None

    self._path = path
    file_list =[x for  x in os.listdir(self._path ) if "out" in x]

    # 'tfpPreNormalizationRay0Polar1'
    for it in file_list:
      # self._one_file(self._path + "\\" + it, it.replace("tfpPreNormalization", ""))
      self._one_file_new(self._path  +it)

    with open(path_filter) as file:
      txt_includes = file.readlines()

    _s0 = " ".join(txt_includes)
    _s0 = _s0.strip().split(" ")
    _s1 = [int(x.strip()) for x in _s0 if (x.strip()).__len__() > 0]
    self.DSignal["filter"]=_s1

    if self.DSignal.__len__()>0:
      with open(name_picle+"/data.pickle", 'wb') as f:
        pickle.dump(self.DSignal, f)

    if not(self._complex in self.DSignal.keys()):
      self.DSignal[self._complex] = [complex(np.float32(self.DSignal["re"]), np.float32(np.float32(self.DSignal["im"])))
                                                    for i in range(len(self.DSignal["im"]))]

    return self.DSignal

  def _one_file(self, path_file, name):
    _ls = []
    _re=[]
    _im=[]
    with open(path_file) as file:
      txt_includes = file.readlines()
      # print(txt_includes)
      for it in txt_includes:
        _ls.extend([x.strip().replace("(","").replace(")","")  for x in it.strip().split(" ")])
      for it in _ls:
        s =it.strip().split(",")
        _re.append(int(s[0].strip()))
        _im.append(int(s[1].strip()))
    self.DSignal[name]={}
    self.DSignal[name]["re"] = _re
    self.DSignal[name]["im"] = _im
    kk=1

  def _one_file_new(self, path_file):
    _ls = []
    _re=[]
    _im=[]
    with open(path_file) as file:
      txt_includes = file.readlines()
      # print(txt_includes)
      for it in txt_includes:
        _ls.extend([x.strip().replace("(","").replace(")","")  for x in it.strip().split(" ")])
      for it in _ls:
        s =it.strip().split(",")
        _re.append(int(s[0].strip()))
        _im.append(int(s[1].strip()))
    self.DSignal={}
    self.DSignal["re"] = _re
    self.DSignal["im"] = _im
    self.DSignal["all"] = np.sqrt(np.pow(_re, 2) + np.pow(_im, 2))
    self.DSignal[self._complex] = [complex(np.float32(_re[i]), np.float32(_im[i])) for i in range(len(_re)) ]
    kk=1

  def To_Json(self, path, data):
    _ls_re = list(data["re"])
    _ls_im = list(data["im"])
    # _ls_all = list(data["all"])
    _dls = {}
    _dls["re"] = _ls_re
    _dls["im"] = _ls_im
    # _dls["all"] = _ls_all

    _text:str = json.dumps(_dls)
    with open(path + "/data.json", 'w') as file:
        file.write(_text)

  def find_file_in_args(self, _path):
    path, dirs, files = next(os.walk(_path))
    if "in_args.txt" in files:
      self._ls_in_args.append(path)
      print(path)
      return
    else:
      _ = [self.find_file_in_args(str(path+"/"+it).replace("//", "/")) for it in dirs]

    # self._path_input

  def convert_standart(self):
    def convertTxtInJson(patn_file, isInt:bool):
      with open(patn_file) as file:
        txt_includes = file.readlines()
        _ls = []
        for it in txt_includes:
          _ls.extend([x.strip().replace("(", "").replace(")", "") for x in it.strip().split(" ")])

        _ls_complex = []
        for it in _ls:
          s = it.strip().split(",")
          if isInt:
            _ls_complex.append((int(s[0].strip()), int(s[1].strip())))
          else:
            _ls_complex.append((float(s[0].strip()), float(s[1].strip())))
      return _ls_complex

    path_out, dirs_out, files_out = next(os.walk(self._path_output))
    if len(dirs_out)==0:
      count_out = 0
    else:
      dirs_out.sort()
      count_out = int(str(dirs_out[len(dirs_out)-1]))
      count_out +=1

    root_dir = Path(self._path_input)

    # Рекурсивно находим все файлы с именем in_args.txt
    # self._ls_in_args = [path.parent for path in root_dir.rglob('in_args.txt')]
    # self._ls_in_args = [path for path in root_dir.rglob('*') if path.is_file() and 'in_args.txt' in path.name]
    # self.find_file_in_args(self._path_input)

    in_args_files = [path for path in root_dir.rglob('in_args.txt')]
    # Получаем уникальные директории, в которых находятся эти файлы
    self._ls_in_args= list(set(path.parent for path in in_args_files))

    count_ls_dir = len(self._ls_in_args)
    for path0 in self._ls_in_args:
      path =str( path0)
      print(f" --- осталось => {count_ls_dir}")
      print(f" ! Select DIR => {path}   !!!")

      _oneBlock = OneBlockDataJson(self._path_output)
      _oneBlock.id = count_out
      # print(f" !!!   Пишим двнные в {self._path_output}   !!!")

      with open(path + "/in_args.txt") as file:
        for it_json in [str(it).replace("\n", "") for it in file.readlines()]:
           s0 = it_json.split("=")
           _oneBlock.in_args_json[s0[0].strip()]= int(s0[1].strip())
      _oneBlock.in_args_json["nl"] = _oneBlock.in_args_json["NL"]
      _oneBlock.in_args_json['true_nihs'] = _oneBlock.in_args_json["trueNihs"]
      _oneBlock.in_args_json['nfgd_fu'] = _oneBlock.in_args_json["nfgdfu"]
      _oneBlock.in_args_json['samples_num'] = _oneBlock.in_args_json["samplesNum"]
      _oneBlock.in_args_json['is_am'] = self._is_am
      del _oneBlock.in_args_json["NL"]
      del _oneBlock.in_args_json["trueNihs"]
      del _oneBlock.in_args_json["nfgdfu"]
      del _oneBlock.in_args_json["samplesNum"]


      with open(path+"/tfpMSeqSigns.txt") as file:
        s = [str(it).replace("\n", "") for it in file.readlines()]
        s1 = [str(it).strip() for it in  (" ".join(s)).split(" ") if len(str(it).strip())>0]
        _oneBlock.tfpMSeqSigns = [int(str(it)) for it in s1]


      # path_data, dirs, files = next(os.walk(path))
      # _path_x0 = str(path_data+"/" + dirs[0]).replace("//", "/")
      # root_dir =  Path(_path_x0)
      # files_with_out = [path for path in root_dir.rglob('*') if path.is_file() and 'out' in path.name]
      # directories_with_out_files = set(path.parent for path in files_with_out)


      files_with_out = [path for path in Path(path).rglob('*') if path.is_file() and 'out' in path.name]
      directories_with_out_files = set(path.parent for path in files_with_out)

      if len(directories_with_out_files)<=0:
        count_ls_dir = count_ls_dir - 1
        print("********   нет файлов OUT...   **************")
        continue

      _path_x1 = list(directories_with_out_files)[0]
      path_data, dirs, files = next(os.walk(_path_x1))
      files = [it for it in files if not("hex" in it)]
      _outs = [it for it in files if "out" in it]
      _ftps = [it for it in files if "tfp" in it]
      _outs.sort()
      _ftps.sort()
      # _oneBlock.out
      number_polar = 0

      print(" ! -> convert => OUT  !!!")

      for it in _outs:
        _path = path_data +"/" + it
        _oneBlock.out["polar" + str(number_polar)] = convertTxtInJson(_path, True)
        number_polar += 1

      try:
        # result = [re.search(r"Ray\d+Polar\d+", s).group(0) for s in _ftps]
        # result = [re.search(r"Polar\d+", s).group(0) for s in _ftps]
        result = [s for s in _ftps if 'Polar' in s]
        # _d_ftps = {(path_data + "/" + _ftps[i]): result[i] for i in range(len(_ftps))}
        _d_ftps = {(path_data + "/" + _ftps[i]): result[i] for i in range(len(result))}
      except:
        print("-------------------  ERROR   --------------------")
        print(" ===  нет  Ray...Polar,,,  ==== ")
        count_ls_dir = count_ls_dir - 1
        continue

      print(" ! -> convert => ftps  !!!")

      for key, value in _d_ftps.items():
        print(value)
        _oneBlock.ftps[value] = convertTxtInJson(key, False)

      _oneBlock.Save()
      count_out = count_out + 1
      count_ls_dir = count_ls_dir -1


  def get_all_file_paths_pathlib(self, directory):
    """Рекурсивно возвращает список путей ко всем файлам (pathlib)."""
    directory_path = Path(directory)
    return [str(entry) for entry in directory_path.rglob("*") if entry.is_file()]

  def find_file_hex_dir(self, files, maska):
    """ Поиск каталога с именем out."""
    for x in  files:
      if len(x)>0:
        path = Path(x)
        if maska is path.name:
          return path.parent
    return ""

  """
  path = Path('/home/user/example.txt')
  
  # Выделяем директорию и файл
  directory = path.parent
  filename = path.name
  
  # Выделяем имя файла без расширения и расширение
  file_stem = path.stem
  file_suffix = path.suffix
  
  print(f"Директория: {directory}")
  print(f"Имя файла: {filename}")
  print(f"Имя файла без расширения: {file_stem}")
  print(f"Расширение файла: {file_suffix}")
  """




'''
with open(_path) as file:
  txt_includes = file.readlines()
  _ls=[]
  for it in txt_includes:
    _ls.extend([x.strip().replace("(", "").replace(")", "") for x in it.strip().split(" ")])

  _ls_complex = []
  for it in _ls:
    s = it.strip().split(",")
    _ls_complex.append(complex(int(s[0].strip()), int(s[1].strip())))

  _oneBlock.out["polar"+str(number_polar)]=_ls_complex
  number_polar+=1
'''
