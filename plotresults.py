from glob import glob
import pickle
import matplotlib.pyplot as plt


def plotbmresults(prefix):
    pklfiles = glob(f"{prefix}-*.pkl")
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

    cpptimes = []
    txtfiles = glob(f"{prefix}-*.txt")
    for fname in txtfiles:
        print(f"Loading from {fname}")
        with open(fname) as res:
            for line in res.readlines():
                if not line:
                    continue
                n, t = line.split(" ")
                cpptimes.append(float(t))
    plt.plot(nums, cpptimes, label="C++ NIX")

    plt.legend(loc="best")
    plt.xlabel("N data arrays")
    plt.ylabel("Cumulative append time (s)")
    plt.savefig(f"{prefix}.png")
    plt.show()
    print("Saved figure times.png")


def main():
    plotbmresults("append")
    plotbmresults("lda")


if __name__ == "__main__":
    main()
