# plate_strict



This document contains JSON examples for plate_strict metadata layouts.


## plate_2wells
(examples:plate_strict:plate_2wells)=

```{code-block} json
:caption: plate_2wells
:linenos:

{
    "zarr_format": 3,
    "node_type": "group",
    "attributes": {
        "ome": {
            "version": "0.5",
            "plate": {
                "acquisitions": [
                    {
                        "id": 1,
                        "maximumfieldcount": 1,
                        "name": "single acquisition",
                        "starttime": 1343731272000
                    }
                ],
                "columns": [
                    {
                        "name": "1"
                    },
                    {
                        "name": "2"
                    },
                    {
                        "name": "3"
                    },
                    {
                        "name": "4"
                    },
                    {
                        "name": "5"
                    },
                    {
                        "name": "6"
                    },
                    {
                        "name": "7"
                    },
                    {
                        "name": "8"
                    },
                    {
                        "name": "9"
                    },
                    {
                        "name": "10"
                    },
                    {
                        "name": "11"
                    },
                    {
                        "name": "12"
                    }
                ],
                "field_count": 1,
                "name": "sparse test",
                "rows": [
                    {
                        "name": "A"
                    },
                    {
                        "name": "B"
                    },
                    {
                        "name": "C"
                    },
                    {
                        "name": "D"
                    },
                    {
                        "name": "E"
                    },
                    {
                        "name": "F"
                    },
                    {
                        "name": "G"
                    },
                    {
                        "name": "H"
                    }
                ],
                "wells": [
                    {
                        "path": "C/5",
                        "rowIndex": 2,
                        "columnIndex": 4
                    },
                    {
                        "path": "D/7",
                        "rowIndex": 3,
                        "columnIndex": 6
                    }
                ]
            }
        }
    }
}
```

## plate_6wells
(examples:plate_strict:plate_6wells)=

```{code-block} json
:caption: plate_6wells
:linenos:

{
    "zarr_format": 3,
    "node_type": "group",
    "attributes": {
        "ome": {
            "version": "0.5",
            "plate": {
                "acquisitions": [
                    {
                        "id": 1,
                        "maximumfieldcount": 2,
                        "name": "Meas_01(2012-07-31_10-41-12)",
                        "starttime": 1343731272000
                    },
                    {
                        "id": 2,
                        "maximumfieldcount": 2,
                        "name": "Meas_02(201207-31_11-56-41)",
                        "starttime": 1343735801000
                    }
                ],
                "columns": [
                    {
                        "name": "1"
                    },
                    {
                        "name": "2"
                    },
                    {
                        "name": "3"
                    }
                ],
                "field_count": 4,
                "name": "test",
                "rows": [
                    {
                        "name": "A"
                    },
                    {
                        "name": "B"
                    }
                ],
                "wells": [
                    {
                        "path": "A/1",
                        "rowIndex": 0,
                        "columnIndex": 0
                    },
                    {
                        "path": "A/2",
                        "rowIndex": 0,
                        "columnIndex": 1
                    },
                    {
                        "path": "A/3",
                        "rowIndex": 0,
                        "columnIndex": 2
                    },
                    {
                        "path": "B/1",
                        "rowIndex": 1,
                        "columnIndex": 0
                    },
                    {
                        "path": "B/2",
                        "rowIndex": 1,
                        "columnIndex": 1
                    },
                    {
                        "path": "B/3",
                        "rowIndex": 1,
                        "columnIndex": 2
                    }
                ]
            }
        }
    }
}
```
