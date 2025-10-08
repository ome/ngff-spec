# multiscales_strict



This document contains JSON examples for multiscales_strict metadata layouts.


## multiscales_example
(examples:multiscales_strict:multiscales_example)=

```{code-block} json
:caption: multiscales_example
:linenos:

{
    "zarr_format": 3,
    "node_type": "group",
    "attributes": {
        "ome": {
            "version": "0.6dev2",
            "multiscales": [
                {
                    "name": "physical",
                    "coordinateSystems": [
                        {
                            "name": "physical",
                            "axes": [
                                {
                                    "name": "t",
                                    "type": "time",
                                    "unit": "millisecond"
                                },
                                {
                                    "name": "c",
                                    "type": "channel"
                                },
                                {
                                    "name": "z",
                                    "type": "space",
                                    "unit": "micrometer"
                                },
                                {
                                    "name": "y",
                                    "type": "space",
                                    "unit": "micrometer"
                                },
                                {
                                    "name": "x",
                                    "type": "space",
                                    "unit": "micrometer"
                                }
                            ]
                        }
                    ],
                    "datasets": [
                        {
                            "path": "0",
                            "coordinateTransformations": [
                                {
                                    "type": "scale",
                                    "scale": [
                                        0.1,
                                        1.0,
                                        0.5,
                                        0.5,
                                        0.5
                                    ],
                                    "input": "0",
                                    "output": "physical"
                                }
                            ]
                        },
                        {
                            "path": "1",
                            "coordinateTransformations": [
                                {
                                    "type": "scale",
                                    "scale": [
                                        0.1,
                                        1.0,
                                        1.0,
                                        1.0,
                                        1.0
                                    ],
                                    "input": "1",
                                    "output": "physical"
                                }
                            ]
                        },
                        {
                            "path": "2",
                            "coordinateTransformations": [
                                {
                                    "type": "scale",
                                    "scale": [
                                        0.1,
                                        1.0,
                                        2.0,
                                        2.0,
                                        2.0
                                    ],
                                    "input": "2",
                                    "output": "physical"
                                }
                            ]
                        }
                    ],
                    "type": "gaussian",
                    "metadata": {
                        "description": "the fields in metadata depend on the downscaling implementation. Here, the parameters passed to the skimage function are given",
                        "method": "skimage.transform.pyramid_gaussian",
                        "version": "0.16.1",
                        "args": "[true]",
                        "kwargs": {
                            "multichannel": true
                        }
                    }
                }
            ]
        }
    }
}
```

## multiscales_example_relative
(examples:multiscales_strict:multiscales_example_relative)=

```{code-block} json
:caption: multiscales_example_relative
:linenos:

{
    "multiscales": [
        {
            "version": "0.5-dev",
            "name": "example",
            "coordinateSystems": [
                {
                    "name": "exampleCoordinateSystem",
                    "axes": [
                        {
                            "name": "t",
                            "type": "time",
                            "unit": "millisecond"
                        },
                        {
                            "name": "c",
                            "type": "channel"
                        },
                        {
                            "name": "z",
                            "type": "space",
                            "unit": "micrometer"
                        },
                        {
                            "name": "y",
                            "type": "space",
                            "unit": "micrometer"
                        },
                        {
                            "name": "x",
                            "type": "space",
                            "unit": "micrometer"
                        }
                    ]
                },
                {
                    "name": "array_0",
                    "axes": [
                        {
                            "name": "t",
                            "type": "time",
                            "unit": "millisecond"
                        },
                        {
                            "name": "c",
                            "type": "channel"
                        },
                        {
                            "name": "z",
                            "type": "space",
                            "unit": "micrometer"
                        },
                        {
                            "name": "y",
                            "type": "space",
                            "unit": "micrometer"
                        },
                        {
                            "name": "x",
                            "type": "space",
                            "unit": "micrometer"
                        }
                    ]
                }
            ],
            "datasets": [
                {
                    "path": "0",
                    "coordinateTransformations": [
                        {
                            "type": "identity",
                            "input": "/0",
                            "output": "array_0"
                        }
                    ]
                },
                {
                    "path": "1",
                    "coordinateTransformations": [
                        {
                            "type": "scale",
                            "scale": [
                                1,
                                1,
                                2,
                                2,
                                2
                            ],
                            "input": "/1",
                            "output": "array_0"
                        }
                    ]
                },
                {
                    "path": "2",
                    "coordinateTransformations": [
                        {
                            "type": "scale",
                            "scale": [
                                1,
                                1,
                                4,
                                4,
                                4
                            ],
                            "input": "/2",
                            "output": "array_0"
                        }
                    ]
                }
            ],
            "coordinateTransformations": [
                {
                    "type": "scale",
                    "scale": [
                        0.1,
                        1.0,
                        0.5,
                        0.5,
                        0.5
                    ],
                    "input": "array_0",
                    "output": "exampleCoordinateSystem"
                }
            ],
            "type": "gaussian",
            "metadata": {
                "description": "the fields in metadata depend on the downscaling implementation. Here, the parameters passed to the skimage function are given",
                "method": "skimage.transform.pyramid_gaussian",
                "version": "0.16.1",
                "args": "[true]",
                "kwargs": {
                    "multichannel": true
                }
            }
        }
    ]
}
```

## multiscales_transformations
(examples:multiscales_strict:multiscales_transformations)=

```{code-block} json
:caption: multiscales_transformations
:linenos:

{
    "zarr_format": 3,
    "node_type": "group",
    "attributes": {
        "ome": {
            "version": "0.5",
            "multiscales": [
                {
                    "axes": [
                        {
                            "name": "y",
                            "type": "space",
                            "unit": "micrometer"
                        },
                        {
                            "name": "x",
                            "type": "space",
                            "unit": "micrometer"
                        }
                    ],
                    "datasets": [
                        {
                            "path": "0",
                            "coordinateTransformations": [
                                {
                                    "scale": [
                                        1,
                                        1
                                    ],
                                    "type": "scale"
                                }
                            ]
                        }
                    ],
                    "coordinateTransformations": [
                        {
                            "scale": [
                                10,
                                10
                            ],
                            "type": "scale"
                        }
                    ],
                    "name": "image_with_coordinateTransformations",
                    "type": "foo",
                    "metadata": {
                        "key": "value"
                    }
                }
            ]
        }
    }
}
```
