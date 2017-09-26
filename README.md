# nix-benchmark
Benchmarks for NIX vs NIXPY

Collection of benchmark scripts for determining the relative performance of NIX vs NIXPY.

Benchmarks:
  1. Create objects (DataArrays) on a Block and append them to a Group.
  2. Create DataArrays with large datasets.

Candidates:
  1. NIX proper.
  2. NIXPY Bindings to C++ (HDF5) backend.
  3. NIXPY PyCore (h5py) backend.
  4. New (optimised) NIXPY without bindings (currently found in the [purest-python](https://github.com/achilleas-k/nixpy/tree/purest-python) branch).
