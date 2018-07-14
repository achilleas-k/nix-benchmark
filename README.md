# nix-benchmark
Benchmarks for NIX vs NIXPY

Collection of benchmark scripts for determining the relative performance of NIX vs NIXPY.

Benchmarks:
  1. Create objects (DataArrays) on a Block and append them to a Group ([append](append)).
  2. Create DataArrays with large datasets ([largeda](largeda)).

Candidates:
  1. NIX (C++).
  2. NIXPY Bindings to C++ (HDF5) backend (v1.4).
  3. NIXPY PyCore (h5py) backend (v1.4).
  4. New (optimised) NIXPY without bindings (currently found in the [new-container](https://github.com/achilleas-k/nixpy/tree/new-container) branch).
  5. H5Py directly.
  6. Neo NixIO with NIXPY v1.4.
  7. Neo NixIO with new NIXPY.

## TODO

DataArray creation benchmark (largeda) should create an empty file each time to avoid counting append or name collision check times.
