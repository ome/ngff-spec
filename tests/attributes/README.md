# Attributes test fixtures

This directory contains JSON files representing the attributes object of a Zarr node.
They can then be validated as much as is possible in isolation
(i.e. without reference to other Zarr nodes, array metadata etc.).

As well as OME-Zarr metadata, they MAY contain a special `_conformance` object with information about the test itself.
So the whole object (minus comments) looks like

```jsonc
{
  "_conformance": {
    // free text describing the feature that a valid case is demonstrating
    // ("name field can be omitted"),
    // or the constraint that an invalid case is violating in positive terms
    // ("should have 5 items", NOT "should not have 3 items")
    "description": "name field can be omitted",
  },
  "ome": {
    // ... OME-Zarr metadata goes here.
  }
}
```

This may be extended in future.

Note that in situ, OME-Zarr metadata's validity may be determined by other Zarr nodes and their metadata.
"Valid" here simply states that the metadata is _internally_ valid.

This is most useful for proving that an implementation can internally represent all valid metadata.
