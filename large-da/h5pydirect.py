import sys
import h5py



h5file = h5py.File("/tmp/data-benchmark-direct.h5")
blk = h5file.create_group("blk")


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
