# transformations



This document contains JSON examples for transformations metadata layouts.


## affine2d2d
(examples:transformations:affine2d2d)=

```{code-block} json
:caption: affine2d2d
:linenos:

{
    "coordinateSystems": [
        {
            "name": "ji",
            "axes": [
                {
                    "name": "j"
                },
                {
                    "name": "i"
                }
            ]
        },
        {
            "name": "yx",
            "axes": [
                {
                    "name": "y"
                },
                {
                    "name": "x"
                }
            ]
        }
    ],
    "coordinateTransformations": [
        {
            "type": "affine",
            "affine": [
                [
                    1,
                    2,
                    3
                ],
                [
                    4,
                    5,
                    6
                ]
            ],
            "input": "ji",
            "output": "yx"
        }
    ]
}
```

## affine2d3d
(examples:transformations:affine2d3d)=

```{code-block} json
:caption: affine2d3d
:linenos:

{
    "coordinateSystems": [
        {
            "name": "ij",
            "axes": [
                {
                    "name": "i"
                },
                {
                    "name": "j"
                }
            ]
        },
        {
            "name": "xyz",
            "axes": [
                {
                    "name": "x"
                },
                {
                    "name": "y"
                },
                {
                    "name": "z"
                }
            ]
        }
    ],
    "coordinateTransformations": [
        {
            "type": "affine",
            "affine": [
                [
                    1,
                    2,
                    3
                ],
                [
                    4,
                    5,
                    6
                ],
                [
                    7,
                    8,
                    9
                ]
            ],
            "input": "ij",
            "output": "xyz"
        }
    ]
}
```

## bijection
(examples:transformations:bijection)=

```{code-block} json
:caption: bijection
:linenos:

{
    "coordinateSystems": [
        {
            "name": "src",
            "axes": [
                {
                    "name": "j"
                },
                {
                    "name": "i"
                }
            ]
        },
        {
            "name": "tgt",
            "axes": [
                {
                    "name": "y"
                },
                {
                    "name": "x"
                }
            ]
        }
    ],
    "coordinateTransformations": [
        {
            "type": "bijection",
            "forward": {
                "type": "coordinates",
                "path": "forward_coordinates"
            },
            "inverse": {
                "type": "coordinates",
                "path": "inverse_coordinates"
            },
            "input": "src",
            "output": "tgt"
        }
    ]
}
```

## bijection_verbose
(examples:transformations:bijection_verbose)=

```{code-block} json
:caption: bijection_verbose
:linenos:

{
    "type": "bijection",
    "forward": {
        "type": "coordinates",
        "path": "forward_coordinates",
        "input": "src",
        "output": "tgt"
    },
    "inverse": {
        "type": "coordinates",
        "path": "inverse_coordinates",
        "input": "tgt",
        "output": "src"
    },
    "input": "src",
    "output": "tgt"
}
```

## byDimension1
(examples:transformations:byDimension1)=

```{code-block} json
:caption: byDimension1
:linenos:

{
    "coordinateSystems": [
        {
            "name": "in",
            "axes": [
                {
                    "name": "j"
                },
                {
                    "name": "i"
                }
            ]
        },
        {
            "name": "out",
            "axes": [
                {
                    "name": "y"
                },
                {
                    "name": "x"
                }
            ]
        }
    ],
    "coordinateTransformations": [
        {
            "type": "byDimension",
            "input": "in",
            "output": "out",
            "transformations": [
                {
                    "type": "translation",
                    "translation": [
                        -1.0
                    ],
                    "input": [
                        "i"
                    ],
                    "output": [
                        "x"
                    ]
                },
                {
                    "type": "scale",
                    "scale": [
                        2.0
                    ],
                    "input": [
                        "j"
                    ],
                    "output": [
                        "y"
                    ]
                }
            ]
        }
    ]
}
```

## byDimension2
(examples:transformations:byDimension2)=

```{code-block} json
:caption: byDimension2
:linenos:

{
    "coordinateSystems": [
        {
            "name": "in",
            "axes": [
                {
                    "name": "l",
                    "type": "array"
                },
                {
                    "name": "j",
                    "type": "array"
                },
                {
                    "name": "k",
                    "type": "array"
                },
                {
                    "name": "i",
                    "type": "array"
                }
            ]
        },
        {
            "name": "out",
            "axes": [
                {
                    "name": "z",
                    "type": "array"
                },
                {
                    "name": "y",
                    "type": "array"
                },
                {
                    "name": "x",
                    "type": "array"
                }
            ]
        }
    ],
    "coordinateTransformations": [
        {
            "type": "byDimension",
            "input": "in",
            "output": "out",
            "transformations": [
                {
                    "type": "translation",
                    "translation": [
                        1,
                        3
                    ],
                    "input": [
                        "i",
                        "k"
                    ],
                    "output": [
                        "y",
                        "x"
                    ]
                },
                {
                    "type": "scale",
                    "scale": [
                        2
                    ],
                    "input": [
                        "j"
                    ],
                    "output": [
                        "z"
                    ]
                }
            ]
        }
    ]
}
```

## byDimensionInvalid1
(examples:transformations:byDimensionInvalid1)=

```{code-block} json
:caption: byDimensionInvalid1
:linenos:

{
    "coordinateSystems": [
        {
            "name": "in",
            "axes": [
                {
                    "name": "j"
                },
                {
                    "name": "i"
                }
            ]
        },
        {
            "name": "out",
            "axes": [
                {
                    "name": "y"
                },
                {
                    "name": "x"
                }
            ]
        }
    ],
    "coordinateTransformations": [
        {
            "type": "byDimension",
            "input": "in",
            "output": "out",
            "transformations": [
                {
                    "type": "translation",
                    "translation": [
                        -1.0
                    ],
                    "input": [
                        "i"
                    ],
                    "output": [
                        "z"
                    ]
                },
                {
                    "type": "scale",
                    "scale": [
                        2.0
                    ],
                    "input": [
                        "0"
                    ],
                    "output": [
                        "y"
                    ]
                }
            ]
        }
    ]
}
```

## byDimensionInvalid2
(examples:transformations:byDimensionInvalid2)=

```{code-block} json
:caption: byDimensionInvalid2
:linenos:

{
    "coordinateSystems": [
        {
            "name": "in",
            "axes": [
                {
                    "name": "j"
                },
                {
                    "name": "i"
                }
            ]
        },
        {
            "name": "out",
            "axes": [
                {
                    "name": "y"
                },
                {
                    "name": "x"
                }
            ]
        }
    ],
    "coordinateTransformations": [
        {
            "type": "byDimension",
            "input": "in",
            "output": "out",
            "transformations": [
                {
                    "type": "translation",
                    "translation": [
                        -1.0
                    ],
                    "input": [
                        "i"
                    ],
                    "output": [
                        "x"
                    ]
                },
                {
                    "type": "scale",
                    "scale": [
                        2.0
                    ],
                    "input": [
                        "i"
                    ],
                    "output": [
                        "x"
                    ]
                }
            ]
        }
    ]
}
```

## byDimensionXarray
(examples:transformations:byDimensionXarray)=

```{code-block} json
:caption: byDimensionXarray
:linenos:

{
    "coordinateSystems": [
        {
            "name": "physical",
            "axes": [
                {
                    "name": "x",
                    "type": "space",
                    "unit": "micrometer"
                },
                {
                    "name": "y",
                    "type": "space",
                    "unit": "micrometer"
                }
            ]
        },
        {
            "name": "array",
            "axes": [
                {
                    "name": "dim_0",
                    "type": "array"
                },
                {
                    "name": "dim_1",
                    "type": "array"
                }
            ]
        }
    ],
    "coordinateTransformations": [
        {
            "type": "byDimension",
            "input": "array",
            "output": "physical",
            "transformations": [
                {
                    "type": "coordinates",
                    "path": "xCoordinates",
                    "input": [
                        "dim_0"
                    ],
                    "output": [
                        "x"
                    ]
                },
                {
                    "type": "coordinates",
                    "path": "yCoordinates",
                    "input": [
                        "dim_1"
                    ],
                    "output": [
                        "y"
                    ]
                }
            ]
        }
    ]
}
```

## coordinates1d
(examples:transformations:coordinates1d)=

```{code-block} json
:caption: coordinates1d
:linenos:

{
    "coordinateSystems": [
        {
            "name": "i",
            "axes": [
                {
                    "name": "i"
                }
            ]
        },
        {
            "name": "x",
            "axes": [
                {
                    "name": "x"
                }
            ]
        }
    ],
    "coordinateTransformations": [
        {
            "name": "a coordinate field transform",
            "type": "coordinates",
            "path": "i2xCoordinates",
            "input": "i",
            "output": "x",
            "interpolation": "nearest"
        }
    ]
}
```

## displacement1d
(examples:transformations:displacement1d)=

```{code-block} json
:caption: displacement1d
:linenos:

{
    "coordinateSystems": [
        {
            "name": "i",
            "axes": [
                {
                    "name": "i"
                }
            ]
        },
        {
            "name": "x",
            "axes": [
                {
                    "name": "x"
                }
            ]
        }
    ],
    "coordinateTransformations": [
        {
            "name": "a displacement field transform",
            "type": "displacements",
            "path": "i2xCoordinates",
            "input": "i",
            "output": "x",
            "interpolation": "nearest"
        }
    ]
}
```

## identity
(examples:transformations:identity)=

```{code-block} json
:caption: identity
:linenos:

{
    "coordinateSystems": [
        {
            "name": "in",
            "axes": [
                {
                    "name": "j"
                },
                {
                    "name": "i"
                }
            ]
        },
        {
            "name": "out",
            "axes": [
                {
                    "name": "y"
                },
                {
                    "name": "x"
                }
            ]
        }
    ],
    "coordinateTransformations": [
        {
            "type": "identity",
            "input": "in",
            "output": "out"
        }
    ]
}
```

## inverseOf
(examples:transformations:inverseOf)=

```{code-block} json
:caption: inverseOf
:linenos:

{
    "coordinateSystems": [
        {
            "name": "moving",
            "axes": [
                {
                    "name": "y-moving"
                },
                {
                    "name": "x-moving"
                }
            ]
        },
        {
            "name": "fixed",
            "axes": [
                {
                    "name": "y-fixed"
                },
                {
                    "name": "x-fixed"
                }
            ]
        }
    ],
    "coordinateTransformations": [
        {
            "type": "inverseOf",
            "transformation": {
                "type": "displacements",
                "path": "path/to/displacements"
            },
            "input": "moving",
            "output": "fixed"
        }
    ]
}
```

## mapAxis1
(examples:transformations:mapAxis1)=

```{code-block} json
:caption: mapAxis1
:linenos:

{
    "coordinateSystems": [
        {
            "name": "in",
            "axes": [
                {
                    "name": "j"
                },
                {
                    "name": "i"
                }
            ]
        },
        {
            "name": "out1",
            "axes": [
                {
                    "name": "y"
                },
                {
                    "name": "x"
                }
            ]
        },
        {
            "name": "out2",
            "axes": [
                {
                    "name": "y"
                },
                {
                    "name": "x"
                }
            ]
        }
    ],
    "coordinateTransformations": [
        {
            "name": "equivalent to identity",
            "type": "mapAxis",
            "mapAxis": {
                "x": "i",
                "y": "j"
            },
            "input": "in",
            "output": "out1"
        },
        {
            "name": "permutation",
            "type": "mapAxis",
            "mapAxis": {
                "y": "i",
                "x": "j"
            },
            "input": "in",
            "output": "out2"
        }
    ]
}
```

## mapAxis2
(examples:transformations:mapAxis2)=

```{code-block} json
:caption: mapAxis2
:linenos:

{
    "coordinateSystems": [
        {
            "name": "in",
            "axes": [
                {
                    "name": "a"
                },
                {
                    "name": "b"
                }
            ]
        },
        {
            "name": "out_down",
            "axes": [
                {
                    "name": "x"
                }
            ]
        },
        {
            "name": "out_up",
            "axes": [
                {
                    "name": "z"
                },
                {
                    "name": "y"
                },
                {
                    "name": "x"
                }
            ]
        }
    ],
    "coordinateTransformations": [
        {
            "name": "projection down",
            "type": "mapAxis",
            "mapAxis": {
                "x": "b"
            },
            "input": "in",
            "output": "out_down"
        },
        {
            "name": "projection up",
            "type": "mapAxis",
            "mapAxis": {
                "z": "b",
                "y": "b",
                "x": "a"
            },
            "input": "in",
            "output": "out_up"
        }
    ]
}
```

## rotation
(examples:transformations:rotation)=

```{code-block} json
:caption: rotation
:linenos:

{
    "coordinateSystems": [
        {
            "name": "ji",
            "axes": [
                {
                    "name": "j"
                },
                {
                    "name": "i"
                }
            ]
        },
        {
            "name": "yx",
            "axes": [
                {
                    "name": "y"
                },
                {
                    "name": "x"
                }
            ]
        }
    ],
    "coordinateTransformations": [
        {
            "type": "rotation",
            "rotation": [
                [
                    0,
                    -1
                ],
                [
                    1,
                    0
                ]
            ],
            "input": "ji",
            "output": "yx"
        }
    ]
}
```

## scale
(examples:transformations:scale)=

```{code-block} json
:caption: scale
:linenos:

{
    "coordinateSystems": [
        {
            "name": "in",
            "axes": [
                {
                    "name": "j"
                },
                {
                    "name": "i"
                }
            ]
        },
        {
            "name": "out",
            "axes": [
                {
                    "name": "y"
                },
                {
                    "name": "x"
                }
            ]
        }
    ],
    "coordinateTransformations": [
        {
            "type": "scale",
            "scale": [
                3.12,
                2
            ],
            "input": "in",
            "output": "out"
        }
    ]
}
```

## sequence
(examples:transformations:sequence)=

```{code-block} json
:caption: sequence
:linenos:

{
    "coordinateSystems": [
        {
            "name": "in",
            "axes": [
                {
                    "name": "j"
                },
                {
                    "name": "i"
                }
            ]
        },
        {
            "name": "out",
            "axes": [
                {
                    "name": "y"
                },
                {
                    "name": "x"
                }
            ]
        }
    ],
    "coordinateTransformations": [
        {
            "type": "sequence",
            "input": "in",
            "output": "out",
            "transformations": [
                {
                    "type": "translation",
                    "translation": [
                        0.1,
                        0.9
                    ]
                },
                {
                    "type": "scale",
                    "scale": [
                        2,
                        3
                    ]
                }
            ]
        }
    ]
}
```

## sequenceSubspace1
(examples:transformations:sequenceSubspace1)=

```{code-block} json
:caption: sequenceSubspace1
:linenos:

{
    "coordinateSystems": [
        {
            "name": "in",
            "axes": [
                {
                    "name": "i"
                },
                {
                    "name": "j"
                }
            ]
        },
        {
            "name": "out",
            "axes": [
                {
                    "name": "x"
                },
                {
                    "name": "y"
                }
            ]
        }
    ],
    "coordinateTransformations": [
        {
            "type": "sequence",
            "input": "in",
            "output": "out",
            "transformations": [
                {
                    "type": "coordinates",
                    "path": "/coordinates",
                    "inputAxes": [
                        "i"
                    ],
                    "outputAxes": [
                        "x"
                    ]
                },
                {
                    "type": "scale",
                    "scale": [
                        2.0
                    ],
                    "inputAxes": [
                        "j"
                    ],
                    "outputAxes": [
                        "y"
                    ]
                }
            ]
        }
    ]
}
```

## translation
(examples:transformations:translation)=

```{code-block} json
:caption: translation
:linenos:

{
    "coordinateSystems": [
        {
            "name": "in",
            "axes": [
                {
                    "name": "j"
                },
                {
                    "name": "i"
                }
            ]
        },
        {
            "name": "out",
            "axes": [
                {
                    "name": "y"
                },
                {
                    "name": "x"
                }
            ]
        }
    ],
    "coordinateTransformations": [
        {
            "type": "translation",
            "input": "in",
            "output": "out",
            "translation": [
                9,
                -1.42
            ]
        }
    ]
}
```

## xarrayLike
(examples:transformations:xarrayLike)=

```{code-block} json
:caption: xarrayLike
:linenos:

{
    "coordinateSystems": [
        {
            "name": "in",
            "axes": [
                {
                    "name": "i",
                    "type": "array"
                },
                {
                    "name": "j",
                    "type": "array"
                }
            ]
        },
        {
            "name": "out",
            "axes": [
                {
                    "name": "x",
                    "type": "space"
                },
                {
                    "name": "y",
                    "type": "space"
                }
            ]
        }
    ],
    "coordinateTransformations": [
        {
            "type": "byDimension",
            "input": "in",
            "output": "out",
            "transformations": [
                {
                    "type": "coordinates",
                    "path": "/xCoordinates",
                    "input": [
                        "i"
                    ],
                    "output": [
                        "x"
                    ]
                },
                {
                    "type": "coordinates",
                    "path": "/yCoordinates",
                    "input": [
                        "j"
                    ],
                    "output": [
                        "y"
                    ]
                }
            ]
        }
    ]
}
```
