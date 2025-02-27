
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from matplotlib import cbook, cm
from matplotlib.colors import LightSource


class Plot3DGraph:
	def __init__(self):
		pass

	def Plot3D_hist(self, d, nHarn):
		if d.__len__()<=0:
			return

		fig = plt.figure()
		ax = fig.add_subplot(projection='3d')

		z=0
		xs = np.arange(nHarn)

		for it in d:
			ys = it[:nHarn]
			ax.bar(xs, ys, zs=z, zdir='y',  alpha=0.8)
			z = z + 1

		ax.set_xlabel('Гармоники')
		ax.set_ylabel('Шаг')
		ax.set_zlabel('Амплитуда')

		plt.show()

	def D3Bar(self, **kwargs):
		_d = kwargs.get("d", None)
		if _d is None:
			return
		_size = _d.shape

		# Данные для осей
		y = np.array([_y for _y in range(_size[0])])
		x = np.array([_x for _x in range(_size[1])])
		# x = np.array([10, 20, 30])  # 3 значения для оси X
		# y = np.array([1, 2, 3, 4, 5])  # 5 значений для оси Y

		# Создаем сетку для 3D графика
		X, Y = np.meshgrid(x, y)  # Создаем сетку для осей
		Z = np.zeros_like(X)  # Исходная высота (0 для всех столбцов)

		# Высоты столбцов (можно задать любые значения, в зависимости от вашей задачи)
		# Z_heights = np.random.randint(1, 10, size=X.shape)  # Случайные высоты для столбцов
		Z_heights = _d # np.random.randint(1, 10, size=X.shape)  # Случайные высоты для столбцов

		# Определение ширины и глубины столбцов
		dx = np.ones_like(Z) * 1  # Ширина столбцов по оси X
		dy = np.ones_like(Z) * 1  # Ширина столбцов по оси Y
		dz = Z_heights  # Высота столбцов

		# Создание фигуры и 3D оси
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')

		# Создание 3D столбчатой диаграммы
		ax.bar3d(X.flatten(), Y.flatten(), Z.flatten(), dx.flatten(), dy.flatten(), dz.flatten(), color='g', alpha=0.7)

		# Настройка заголовков и меток
		ax.set_title('3D Bar Chart with Different X and Y Lengths')
		ax.set_xlabel('X-axis')
		ax.set_ylabel('Y-axis')
		ax.set_zlabel('Z-axis')

		# Отображение графика
		plt.show()

	def Surface(self, **kwargs):
		_d = kwargs.get("d", None)
		if _d is None:
			return
		_size = _d.shape

		z = _size
		nrows, ncols = _d.shape

		y = np.array([_y for _y in range(_size[0])])
		x = np.array([_x for _x in range(_size[1])])

		x, y = np.meshgrid(x, y)

		region = np.s_[0:_size[1], 0:_size[0]]
		x, y, z = x[region], y[region], z[region]

		# Set up plot
		fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))

		ls = LightSource(270, 45)
		# To use a custom hillshading mode, override the built-in shading and pass
		# in the rgb colors of the shaded surface calculated from "shade".
		rgb = ls.shade(z, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
		surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=rgb,
													 linewidth=0, antialiased=False, shade=False)

		plt.show()