import os
import sys
import pickle
import matplotlib.pyplot as plt
from tempfile import TemporaryDirectory

import nixio as nixio14
import nixionew
import h5py
import neo
from append import append
# from largeda import largeda


tmpdir = TemporaryDirectory(prefix="nixbenchmarks")
tmpfile = os.path.join(tmpdir.name, "nixbench.nix")


def run(test, N):
    res = dict()
    print("Running nixio14/h5py")
    nf = nixio14.File.open(tmpfile,
                           mode=nixio14.FileMode.Overwrite,
                           backend="h5py")
    times = test.runtest(nf, N)
    res["nixio14/h5py"] = times
    nf.close()

    print("Running nixio14/hdf5")
    nf = nixio14.File.open(tmpfile,
                           mode=nixio14.FileMode.Overwrite,
                           backend="hdf5")
    times = test.runtest(nf, N)
    res["nixio14/hdf5"] = times
    nf.close()

    print("Running nixionew")
    nf = nixionew.File.open(tmpfile,
                            mode=nixionew.FileMode.Overwrite)
    times = test.runtest(nf, N)
    res["nixionew"] = times
    nf.close()

    print("Running nix(C++)")
    times = test.runtest_nix(N)
    res["nix(C++)"] = times

    print("Running h5py")
    hf = h5py.File(tmpfile, mode="w")
    times = test.runtest_h5py(hf, N)
    res["h5py"] = times
    hf.close()

    print("Running neo/nixio14")
    neo.io.nixio.nix = nixio14
    io = neo.NixIO(tmpfile, mode="ow")
    times = test.runtest_neo(io, N)
    res["neo/nixio14"] = times
    io.close()

    print("Running neo/nixionew")
    neo.io.nixio.nix = nixionew
    io = neo.NixIO(tmpfile, mode="ow")
    times = test.runtest_neo(io, N)
    res["neo/nixionew"] = times
    io.close()

    return res


def plot_results(res, title="", xlabel=""):
    for name, times in res.items():
        plt.plot(*times, label=name)
    plt.legend()
    plt.title(title)
    plt.legend(loc="best")
    plt.xlabel(xlabel)
    plt.ylabel("Write time (s)")
    figname = os.path.join("results", f"{title}.png")
    print(f"Saving plot to {figname}")
    plt.savefig(figname)
    plt.show()


def main(N):
    res = run(append, N)
    plot_results(res, title="append", xlabel="N data arrays")
    filename = "results.pkl"
    with open(filename, "wb") as fp:
        print(f"Saving results to {filename}")
        pickle.dump(res, fp)

    # res = run(largeda, N*10)
    # plot_results(res, title="large DA", xlabel="DA size")
    # filename = "largeda.pkl"
    # with open(filename, "wb") as fp:
    #     print(f"Saving results to {filename}")
    #     pickle.dump(res, fp)


if __name__ == "__main__":
    N = int(sys.argv[1])
    main(N)
