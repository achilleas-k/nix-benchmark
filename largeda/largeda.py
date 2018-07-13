import h5py
from time import time
import numpy as np


def runtest(nixfile, N):
    blk = nixfile.create_block("blk", "blk")
    times = []
    for n in range(N):
        data = np.random.random(n)
        name = "data" + str(n)
        # blk.create_data_array(name, "test", data=data)
        da = blk.create_data_array(name, "test", shape=(n,))
        t0 = time()  # measure write data time only!
        da.write_direct(data)
        t1 = time()
        times.append(t1-t0)
    return times


def benchmarkdirect(N):
    h5file = h5py.File("/tmp/append-benchmark-direct.nix", "w")
    blk = h5file.create_group("blk")
    times = []
    for n in range(N):
        data = np.random.random(n)
        name = "data" + str(n)
        t0 = time()
        da = blk.create_group(name)
        dataset = da.require_dataset(
            name, shape=(n,), dtype=data.dtype,
            chunks=True, maxshape=(None,)
        )
        dataset[:] = data
        t1 = time()
        times.append(t1-t0)
    h5file.close()
    return times
