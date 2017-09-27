import sys
import nixio as nix
from time import time
from uuid import uuid4
import numpy as np
import pickle


def verify_file(backend, N):
    print("Verifying file")
    nixfile = nix.File.open("/tmp/append-test.h5", nix.FileMode.ReadOnly)
    blk = nixfile.blocks["blk"]
    assert blk.type == "blk"
    grp = blk.groups["grp"]
    assert grp.type == "grp"
    assert len(blk.data_arrays) == N
    assert len(grp.data_arrays) == N
    nixfile.close()


def create_and_append(nixfile):
    blk = nixfile.blocks[0]
    grp = blk.groups[0]
    # prepending stuff to uuid because having a uuid as name confuses NIX
    da = blk.create_data_array("da" + uuid4().hex, "da", data=[])
    t0 = time()
    grp.data_arrays.append(da)
    return time()-t0


def runtest(backend, N):
    nixfile = nix.File.open("/tmp/append-benchmark.nix",
                            nix.FileMode.Overwrite,
                            backend=backend)
    blk = nixfile.create_block("blk", "blk")
    blk.create_group("grp", "grp")
    times = []
    for n in range(N):
        times.append(create_and_append(nixfile))
    nixfile.close()
    # verify_file(backend, N)
    return times


def main(N, filename=None):
    if filename is None:
        filename = "appendresults.pkl"
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
