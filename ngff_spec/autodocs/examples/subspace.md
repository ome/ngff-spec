# subspace



This document contains JSON examples for subspace metadata layouts.


## subspaceMultidim
(examples:subspace:subspaceMultidim)=

```{code-block} json
:caption: subspaceMultidim
:linenos:

{
    "coordinateSystems": [
        {
            "name": "in",
            "axes": [
                {
                    "name": "0",
                    "type": "array"
                },
                {
                    "name": "1",
                    "type": "array"
                },
                {
                    "name": "2",
                    "type": "array"
                },
                {
                    "name": "3",
                    "type": "array"
                },
                {
                    "name": "4",
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
                },
                {
                    "name": "z",
                    "type": "space"
                }
            ]
        }
    ],
    "coordinateTransformations": [
        {
            "type": "byDimension",
            "name": "5D-to-3D-not-contiguous",
            "input": "in",
            "output": "out",
            "transformations": [
                {
                    "type": "mapAxis",
                    "mapAxis": {
                        "0": "x",
                        "2": "z"
                    },
                    "input": [
                        "0",
                        "2"
                    ],
                    "output": [
                        "x",
                        "z"
                    ]
                },
                {
                    "type": "scale",
                    "scale": [
                        2
                    ],
                    "input": [
                        "1"
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

## subspacePermute
(examples:subspace:subspacePermute)=

```{code-block} json
:caption: subspacePermute
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
            "type": "byDimension",
            "input": "in",
            "output": "out",
            "transformations": [
                {
                    "type": "identity",
                    "input": [
                        "j"
                    ],
                    "output": [
                        "x"
                    ]
                },
                {
                    "type": "scale",
                    "scale": [
                        2
                    ],
                    "input": [
                        "i"
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
