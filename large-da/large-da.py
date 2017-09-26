import nixio as nix
from time import time
import matplotlib.pyplot as plt
import numpy as np
from subprocess import check_output


def writepy(N):
    nixfile = nix.File.open("/tmp/large-da-test.h5", nix.FileMode.Overwrite)
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


def runcpp(N):
    out = check_output(["./largeda", str(N)])
    times = []
    for line in out.split(b"\n"):
        if not line:
            continue
        n, t = line.split(b" ")
        times.append(float(t))
    return times


def main():
    N = 1000
    ptimes = writepy(N)
    btimes = runcpp(N)
    ptimes = np.cumsum(ptimes)
    btimes = np.cumsum(btimes)
    nums = range(1, N+1)
    for idx, p, b in zip(nums, ptimes, btimes):
        print("{:3d}: {:6.5f}    {:6.5f}".format(idx, p, b))

    p_linear = np.array(nums) * (ptimes[-1] / nums[-1])
    b_linear = np.array(nums) * (btimes[-1] / nums[-1])
    plt.figure()
    plt.plot(nums, p_linear, "k--")
    plt.plot(nums, ptimes, label="Python")
    plt.plot(nums, b_linear, "k-.")
    plt.plot(nums, btimes, label="C++")
    plt.legend(loc="best")
    plt.xlabel("len(DataArray)")
    plt.ylabel("Cumulative append time (s)")
    plt.savefig("times.png")
    print("Saved figure times.png")


if __name__ == "__main__":
    main()
