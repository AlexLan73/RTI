import numpy as np
from Graphs.Core.Plot3D import Plot3DGraph
_plot = Plot3DGraph()

matrix = np.random.randint(0, 1000, size=(1000, 15))

indy = np.array([_y for _y in range(matrix.shape[0])])
indx = np.array([_x for _x in range(matrix.shape[1])])


for it in indx:
	v0 = matrix[:,it]
	v0 = [int(v0[i]/(i+1)) for i in indy]
	matrix[:, it] = np.array(v0)
# _plot.D3Bar(d= matrix)
_plot.Surface(d= matrix)
stop=1