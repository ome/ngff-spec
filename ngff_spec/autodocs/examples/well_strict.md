# well_strict



This document contains JSON examples for well_strict metadata layouts.


## well_2fields
(examples:well_strict:well_2fields)=

```{code-block} json
:caption: well_2fields
:linenos:

{
    "zarr_format": 3,
    "node_type": "group",
    "attributes": {
        "ome": {
            "version": "0.5",
            "well": {
                "images": [
                    {
                        "acquisition": 0,
                        "path": "0"
                    },
                    {
                        "acquisition": 3,
                        "path": "1"
                    }
                ]
            }
        }
    }
}
```

## well_4fields
(examples:well_strict:well_4fields)=

```{code-block} json
:caption: well_4fields
:linenos:

{
    "zarr_format": 3,
    "node_type": "group",
    "attributes": {
        "ome": {
            "version": "0.5",
            "well": {
                "images": [
                    {
                        "acquisition": 1,
                        "path": "0"
                    },
                    {
                        "acquisition": 1,
                        "path": "1"
                    },
                    {
                        "acquisition": 2,
                        "path": "2"
                    },
                    {
                        "acquisition": 2,
                        "path": "3"
                    }
                ]
            }
        }
    }
}
```
