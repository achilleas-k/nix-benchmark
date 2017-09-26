import sys
import nixio as nix
from time import time
from uuid import uuid4
import numpy as np
from subprocess import check_output
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
    nixfile = nix.File.open("/tmp/append-test.h5", nix.FileMode.Overwrite,
                            backend=backend)
    blk = nixfile.create_block("blk", "blk")
    blk.create_group("grp", "grp")
    times = []
    for n in range(N):
        times.append(create_and_append(nixfile))
    nixfile.close()
    # verify_file(backend, N)
    return times


def runcpp(N):
    out = check_output(["./append", str(N)])
    times = []
    for line in out.split(b"\n"):
        if not line:
            continue
        n, t = line.split(b" ")
        times.append(float(t))
    return times


def main(filename=None):
    print(f"Running tests with {nix.__file__}")
    N = 10000
    N = 500
    ptimes = runtest("h5py", N)
    btimes = runtest("hdf5", N)
    # ctimes = runcpp(N)
    ptimes = np.cumsum(ptimes)
    btimes = np.cumsum(btimes)
    if filename is None:
        filename = "results.pkl"

    with open(filename, "wb") as fp:
        print(f"Saving results to {filename}")
        pickle.dump({
            "h5py": ptimes,
            "hdf5": btimes,
        }, fp)


if __name__ == "__main__":
    fname = sys.argv[1]
    main(fname)
