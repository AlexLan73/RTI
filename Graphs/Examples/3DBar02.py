import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Создаем объем данных
x = np.array([ 10, 20, 30, 40, 50, 60]) # , 60, 70
y = np.array([ 1, 2, 3, 4, 5])
z = np.zeros_like(x)  # Начальная высота каждого столбика

# Высоты столбиков (случайные значения или ваши данные)
dz = np.random.randint(1, 10, size=x.shape)  # Случайные высоты от 1 до 10

# Ширина столбиков
dx = dy = 0.5  # Ширина и глубина

# Создаем 3D-график
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Создаем столбцы
ax.bar3d(y, x,  z, dx, dy, dz, color='b', zsort='average')

# Настраиваем метки и заголовок
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Height')
ax.set_title('3D Bar Plot Example')

# Отображаем график
plt.show()