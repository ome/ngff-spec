# OME-NGFF file format specification

NGFF is an initiative by the bioimaging community to develop imaging format specifications to
address issues of scalability and interoperability.

This repository contains the central [specification text](./ngff_spec/specification.md),
a comprehensive list of [metadata examples](./ngff_spec/examples)
as well as [json schemas](./ngff_spec/schemas) to validate written ome-zarr image data.

The built documentation including contribution hints can be found **[here](https://ngff-spec.readthedocs.io/en/latest/specification.html)**.

## Conformance tests

Conformance can be tested at several levels.

1. Validating that individual fields of a zarr attributes object are valid.
2. Validating a single zarr attributes object (i.e. containing OME-Zarr metadata)

    - Validates that correct data can be represented, and that internally inconsistent data can be caught
    - Cannot validate references to other objects in the zarr hierarchy
    - Cannot validate conformance to other zarr metadata e.g. array data type, dimensionality

3. Validating a metadata-only zarr hierarchy

    - Can validate references to other objects and other zarr metadata
    - Cannot validate values e.g. the invertibility of an affine matrix defined as a zarr array

4. Validating a zarr hierarchy with data

This repository contains

- JSON schemas which handle level 1
- a set of test zarr attributes JSON for level 2 ([`./tests/attributes`](./tests/attributes/))
- a set of metadata-only zarr hierarchies for level 3 ([`./tests/zarr`](./tests/zarr/))

as well as a tool for feeding these test cases into an external validator.

### Testing tool

See [`ome_zarr_conformance.py`](./ome_zarr_conformance.py).

Run it in either `attributes` or `zarr` mode, optionally with filters for test names or types.

Wrap your own OME-Zarr implementation in a
["dingus"](https://talk.commonmark.org/t/origin-of-the-usage-for-dingus/1226) CLI,
which takes as its last argument the path to either

- attributes mode: a JSON file representing zarr attributes (i.e. containing OME-Zarr metadata)
- zarr mode: a zarr hierarchy root on the file system (i.e. a directory containing `zarr.json`)

The dingus should print to STDOUT a JSON object with the keys:

- `"valid"`: boolean, whether this is valid
- optionally `"message"`: string, free text describing the success/ failure

Call the tool like

```sh
python3 ./ome_zarr_conformance.py attributes -- path/to/my/dingus -dingusArg +argValue 10
```

Each call to the dingus will then look like

```sh
>>> path/to/my/dingus -dingusArg +argValue 10 /home/you/ngff-spec/tests/attributes/spec/valid/custom_type_axes.json

{"valid": true}
```

`ome_zarr_conformance.py` will parse the JSON output and format the results of all requested tests in a tab-separated table.

Full usage information is available with `./ome_zarr_conformance.py --help`.

### JSON Schema tests

You can use the conformance testing tool to test JSON Schema-based validation with

```sh
>>> ./ome_zarr_conformance.py attributes -- uv run jsonschema_dingus.py attributes
```

Some failures are expected as JSON Schema can only handle level 1 validation.
