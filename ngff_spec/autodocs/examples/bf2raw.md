# bf2raw



This document contains JSON examples for bf2raw metadata layouts.


## image
(examples:bf2raw:image)=

```{code-block} json
:caption: image
:linenos:

{
    "zarr_format": 3,
    "node_type": "group",
    "attributes": {
        "ome": {
            "version": "0.5",
            "bioformats2raw.layout": 3
        }
    }
}
```

## plate
(examples:bf2raw:plate)=

```{code-block} json
:caption: plate
:linenos:

{
    "zarr_format": 3,
    "node_type": "group",
    "attributes": {
        "ome": {
            "version": "0.5",
            "bioformats2raw.layout": 3,
            "plate": {
                "columns": [
                    {
                        "name": "1"
                    }
                ],
                "name": "Plate Name 0",
                "wells": [
                    {
                        "path": "A/1",
                        "rowIndex": 0,
                        "columnIndex": 0
                    }
                ],
                "field_count": 1,
                "rows": [
                    {
                        "name": "A"
                    }
                ],
                "acquisitions": [
                    {
                        "id": 0
                    }
                ]
            }
        }
    }
}
```
