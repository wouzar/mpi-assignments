import numpy as np
from mpi4py import MPI
from functools import reduce
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
LENGTH = 3

if rank == 0:
    matrix = np.random.rand(LENGTH, LENGTH)
    print('matrix:')
    print(matrix)
    to_sum = [np.append(x,y) for x, y in zip(matrix, matrix.T)]
    all_data = reduce(lambda x,y: np.append(x,y), to_sum)
else:
    matrix = None
    _list = None
    all_data = None

data = np.zeros(LENGTH * 2)

comm.Scatter(all_data, data, root=0)

sums = sum(data)
newData = comm.gather(sums, root=0)

if rank == 0:
	di = np.diag_indices(LENGTH)
	matrix[di] = newData - matrix[di]
	print('result matrix:')
	print(matrix)
