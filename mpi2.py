import numpy as np
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


def prettify(arr):
	out = ''
	for i in range(0, rows):
		for j in range(0, columns):
			out += repr(array[i][j]) + " "
		out += '\n'
	return out
	


rows = 3
columns = 4
array = [ [ 5, 2, 3, 3 ],[ 1, 6, 1, 5 ],[ 3, -4, -2, 8 ] ]



ileft = int(rank * (rows / size))
iright = int(rank * (rows / size) + (rows / size))

length = int(rows / size)


for i in range(ileft, iright):
	for j in range(0, i):
		value = array[j][j]
		for k in range(columns - 1, -1, -1):
			array[i][k] -= array[j][k] * array[i][j]
	

	for j in range(0, i):
		value = array[i][i]
		for k in range(columns - 1, -1, -1):
			array[j][k] -= array[i][k] * array[j][i] / value

	value = array[i][i]

	for j in range(columns - 1, -1, -1):
		array[i][j] /= value

foo = np.copy(array)
if rank == 0:
		
	for i in range(1, size):
		left = int(i * (rows / size))
		right = int(i * (rows / size) + (rows / size))
		comm.Recv(foo, source=i)
		for i in range(left, right):
			for j in range(0, i):
				for k in range(columns - 1, -1, -1):
					array[i][k] = foo[i][k]
else:
	comm.Send(np.array(foo), dest=0)

if rank == 0:	
	print(prettify(array))
