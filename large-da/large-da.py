import sys
import h5py
import nixio as nix
from time import time
import numpy as np
import pickle


def runtest(backend, N):
    nixfile = nix.File.open(f"/tmp/data-benchmark-{backend}.nix",
                            nix.FileMode.Overwrite,
                            backend=backend)
    blk = nixfile.create_block("blk", "blk")
    times = []
    for n in range(N):
        data = np.random.random(n)
        name = "data" + str(n)
        # blk.create_data_array(name, "test", data=data)
        t0 = time()
        da = blk.create_data_array(name, "test", shape=(n,))
        da.write_direct(data)
        t1 = time()
        times.append(t1-t0)
    nixfile.close()
    return times


def benchmarkdirect(N):
    h5file = h5py.File("/tmp/append-benchmark-direct.h5", "w")
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


def main(N, filename=None):
    if filename is None:
        filename = "ldaresults.pkl"
    print(f"Loaded {nix.__file__}")
    ptimes = runtest("h5py", N)
    ptimes = np.cumsum(ptimes)
    if "cpp" in filename:
        btimes = runtest("hdf5", N)
        btimes = np.cumsum(btimes)
        htimes = benchmarkdirect(N)
        htimes = np.cumsum(htimes)

    with open(filename, "wb") as fp:
        results = {"h5py": ptimes}
        if "cpp" in filename:
            results["hdf5"] = btimes
            results["h5direct"] = htimes
        print(f"Saving results to {filename}")
        pickle.dump(results, fp)


if __name__ == "__main__":
    N = int(sys.argv[1])
    fname = sys.argv[2]
    main(N, fname)
