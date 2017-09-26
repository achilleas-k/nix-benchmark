import sys
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


def main(N, filename=None):
    if filename is None:
        filename = "ldaresults.pkl"
    print(f"Loaded {nix.__file__}")
    ptimes = runtest("h5py", N)
    ptimes = np.cumsum(ptimes)
    if "cpp" in filename:
        btimes = runtest("hdf5", N)
        btimes = np.cumsum(btimes)

    with open(filename, "wb") as fp:
        print(f"Saving results to {filename}")
        if "cpp" in filename:
            pickle.dump({"h5py": ptimes, "hdf5": btimes}, fp)
        else:
            pickle.dump({"h5py": ptimes}, fp)


if __name__ == "__main__":
    N = int(sys.argv[1])
    fname = sys.argv[2]
    main(N, fname)
