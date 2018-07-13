from time import time
from uuid import uuid4
import numpy as np


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
    t0 = time()
    grp.data_arrays.append(da)
    return time()-t0


def runtest(nixfile, N):
    blk = nixfile.create_block("blk", "blk")
    blk.create_group("grp", "grp")
    times = []
    for n in range(N):
        times.append(create_and_append(nixfile))
    verify_file(nixfile, N)
    return np.cumsum(times)
