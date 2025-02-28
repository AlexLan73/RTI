import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Данные для осей
x = np.array([10, 20, 30])             # 3 значения для оси X
y = np.array([1, 2, 3, 4, 5, 6, 7, 8])          # 5 значений для оси Y

# Создаем сетку для 3D графика
X, Y = np.meshgrid(x, y)               # Создаем сетку для осей
Z = np.zeros_like(X)                   # Исходная высота (0 для всех столбцов)

# Высоты столбцов (можно задать любые значения, в зависимости от вашей задачи)
Z_heights = np.random.randint(1, 10, size=X.shape)  # Случайные высоты для столбцов

# Определение ширины и глубины столбцов
dx = np.ones_like(Z) * 5             # Ширина столбцов по оси X
dy = np.ones_like(Z) * 1             # Ширина столбцов по оси Y
dz = Z_heights                        # Высота столбцов

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