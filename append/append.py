from time import time
from uuid import uuid4
import numpy as np
import neo
import quantities as pq
from subprocess import check_output


def verify_file(nixfile, N):
    print("Verifying file")
    blk = nixfile.blocks["blk"]
    assert blk.type == "blk"
    grp = blk.groups["grp"]
    assert grp.type == "grp"
    assert len(blk.data_arrays) == N
    assert len(grp.data_arrays) == N


def create_and_append(nixfile):
    blk = nixfile.blocks[0]
    grp = blk.groups[0]
    # prepending stuff to uuid because having a uuid as name confuses NIX
    da = blk.create_data_array("da" + uuid4().hex, "da", data=[])
    t0 = time()  # measure append time only!
    grp.data_arrays.append(da)
    return time()-t0


def runtest(nixfile, N):
    blk = nixfile.create_block("blk", "blk")
    blk.create_group("grp", "grp")
    times = []
    for n in range(N):
        times.append(create_and_append(nixfile))
        print(f" :: {n}/{N} {int(n/N*100):3d}%", end="\r")
    verify_file(nixfile, N)
    times = np.cumsum(times)
    print(f" :: Total time: {times[-1]:7.05f} s")
    return list(range(N)), times


def create_and_append_h5py(hfile):
    blk = hfile["blk"]
    grp = blk["grp"]
    name = "da" + uuid4().hex
    da = blk.create_dataset(name, (1,))
    t0 = time()
    grp[name] = da
    return time()-t0


def runtest_h5py(hfile, N):
    blk = hfile.create_group("blk")
    blk.create_group("grp")
    times = []
    for n in range(N):
        times.append(create_and_append_h5py(hfile))
        print(f" :: {n}/{N} {int(n/N*100):3d}%", end="\r")
    times = np.cumsum(times)
    print(f" :: Total time: {times[-1]:7.05f} s")
    return list(range(N)), times


def runtest_neo(io, N):
    times = []
    blk = neo.Block()
    seg = neo.Segment()
    blk.segments.append(seg)
    step = 1
    if N >= 10:
        step = N//10
    Ns = list()
    for n in range(0, N, step):
        seg.analogsignals = []
        for ni in range(n):
            seg.analogsignals.append(neo.AnalogSignal(signal=[0],
                                                      units="V",
                                                      sampling_rate=1 * pq.Hz))
        t0 = time()
        io.write_block(blk)
        times.append(time() - t0)
        Ns.append(n)
        print(f" :: {n}/{N} {int(n/N*100):3d}%", end="\r")
    verify_file(io.nixfile, N)
    print(f" :: Last write time: {times[-1]:7.05f} s")
    return Ns, times


def runtest_nix(N):
    times = check_output([f"./append/append", str(N)],
                         env={"LD_LIBRARY_PATH": "/usr/local/lib"})
    times = [float(t.split(b", ")[1]) for t in times.splitlines()]
    print(f" :: Total time: {times[-1]:7.05f} s")
    return list(range(N)), times
