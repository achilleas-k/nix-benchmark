import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt


def main():
    pklfiles = sys.argv[1:]
    results = {}
    for fname in pklfiles:
        print(f"Loading from {fname}")
        with open(fname, "rb") as pf:
            res = pickle.load(pf)
        results[fname] = res

    N = len(results[pklfiles[0]]["h5py"])
    nums = range(1, N+1)

    plt.figure()
    for fname in pklfiles:
        for k in results[fname]:
            plt.plot(nums, results[fname][k], label=f"{fname} - {k}")

    plt.legend(loc="best")
    plt.xlabel("N data arrays")
    plt.ylabel("Cumulative append time (s)")
    plt.savefig("times.png")
    print("Saved figure times.png")


if __name__ == "__main__":
    main()
