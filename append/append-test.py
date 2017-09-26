import nixio as nix
from time import time
from uuid import uuid4
import matplotlib.pyplot as plt
import numpy as np
from subprocess import check_output


def verify_file(backend, N):
    print("Verifying file")
    nixfile = nix.File.open("/tmp/append-test.h5", nix.FileMode.ReadOnly,
                            backend=backend)
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
    verify_file(backend, N)
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


N = 10000
ptimes = runtest("h5py", N)
# btimes = runtest("hdf5", N)
btimes = runcpp(N)
ptimes = np.cumsum(ptimes)
# btimes = np.cumsum(btimes)

nums = range(1, N+1)
for idx, p, b in zip(nums, ptimes, btimes):
    print("{:3d}: {:6.5f}    {:6.5f}".format(idx, p, b))

p_linear = np.array(nums) * (ptimes[-1] / nums[-1])
b_linear = np.array(nums) * (btimes[-1] / nums[-1])
plt.figure()
# plt.ylim(0, 1.5)
plt.plot(nums, p_linear, "k--")
plt.plot(nums, ptimes, label="Python")
plt.plot(nums, b_linear, "k-.")
plt.plot(nums, btimes, label="C++")
plt.legend(loc="best")
plt.xlabel("N data arrays")
plt.ylabel("Cumulative append time (s)")
plt.savefig("times.png")
print("Saved figure times.png")
