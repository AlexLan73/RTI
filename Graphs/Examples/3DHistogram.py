
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Создаем данные для гистограммы
x = np.random.choice([1, 2, 3, 4, 5], size=100)
y = np.random.choice([1, 2, 3, 4, 5], size=100)
z = np.zeros_like(x)

# Подсчитываем количество элементов для каждой пары (x, y)
hist, xedges, yedges = np.histogram2d(x, y, bins=(5, 5))

# Создаем координаты для вершин гистограммы
xpos, ypos = np.meshgrid(xedges[:-1] + 0.5, yedges[:-1] + 0.5, indexing="ij")
xpos = xpos.ravel()
ypos = ypos.ravel()
zpos = 0

# Высота гистограммы соответствует количеству элементов
dx = dy = 0.5 * np.ones_like(zpos)
dz = hist.ravel()

# Создаем 3D-график
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')

# Настраиваем метки и заголовок
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Count')
ax.set_title('3D Histogram Example')

# Показываем график
plt.show()