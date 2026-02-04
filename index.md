---
title: Next-generation file format specification
short_title: OME-Zarr
---

# 🚧 Dev: 0.6.dev3 🚧
(ngff-spec:spec:head)=

**Feedback:** [Forum](https://forum.image.sc/tag/ome-ngff), [Github](https://github.com/ome/ngff/issues)

**Editor:** Josh Moore, ([German BioImaging e.V.](https://gerbi-gmb.de)), [<img src="https://upload.wikimedia.org/wikipedia/commons/0/06/ORCID_iD.svg" alt="ORCID iD" height=12 width=12 style="vertical-align: middle;"/>](https://orcid.org/0000-0003-4028-811X)

## Abstract

```{warning}
This is **not** the released version of the ngff-specification.
It is a work-in-progress document.
Upon release, this warning will be removed and the version number in the document updated.

```

This document contains next-generation file format (NGFF) specifications for storing bioimaging data in the cloud.
All specifications are submitted to the <https://image.sc> community for review.

## Status of This Document

The working title version of this specification is 0.6.dev3.
Migration scripts will be provided between numbered versions.
Data written with these latest changes (an "editor's draft") will not necessarily be supported.

The conventions and specifications defined in this document
are designed to enable next-generation file formats to represent
the same bioimaging data that can be represented in [OME-TIFF](http://www.openmicroscopy.org/ome-files/) and beyond.

## Document conventions

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL”
are to be interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

<p>
<dfn>Transitional</dfn> metadata is added to the specification with the intention of removing it in the future.
Implementations may be expected (MUST) or encouraged (SHOULD) to support the reading of the data,
but writing will usually be optional (MAY).
Examples of transitional metadata include custom additions by implementations that are later submitted as a formal specification.
(See [bioformats2raw](bf2raw))
</p>

Some of the JSON examples in this document include comments.
However, these are only for clarity purposes and comments MUST NOT be included in JSON objects.

## Storage format

OME-Zarr is implemented using the Zarr format as defined by the
[version 3 of the Zarr specification](https://zarr-specs.readthedocs.io/en/latest/v3/core/v3.0.html).
All features of the Zarr format including codecs, chunk grids, chunk key encodings, data types and storage transformers
MAY be used with OME-Zarr unless explicitly disallowed in this specification.

An overview of the layout of an OME-Zarr fileset should make understanding the following metadata sections easier.
The hierarchy is represented here as it would appear locally
but could equally be stored on a web server to be accessed via HTTP or in object storage like S3 or GCS.

### Images

The following layout describes the expected Zarr hierarchy for images with multiple levels of resolutions and optionally associated labels.
Note that the number of dimensions is variable between 2 and 5 and that axis names are arbitrary, see [multiscales metadata](#multiscales-md) for details.

```text
├── 123.zarr                  # One OME-Zarr image (id=123).
│   ...
│
└── 456.zarr                  # Another OME-Zarr image (id=456).
    │
    ├── zarr.json             # Each image is a Zarr group of other groups and arrays.
    │                         # Group level attributes are stored in the `zarr.json` file and include
    │                         # "multiscales" and "omero" (see below).
    │
    ├── 0                     # Each multiscale level is stored as a separate Zarr array,
    │   ...                   # which is a folder containing chunk files which compose the array.
    ├── n                     # The name of the array is arbitrary with the ordering defined by
    │   │                     # by the "multiscales" metadata, but is often a sequence starting at 0.
    │   │
    │   ├── zarr.json         # All image arrays must be up to 5-dimensional
    │   │                     # with the axis of type time before type channel, before spatial axes.
    │   │
    │   └─ ...                # Chunks are stored conforming to the Zarr array specification and 
    │                         # metadata as specified in the array's `zarr.json`.
    │
    └── labels
        │
        ├── zarr.json         # The labels group is a container which holds a list of labels to make the objects easily discoverable
        │                     # All labels will be listed in `zarr.json` e.g. `{ "labels": [ "original/0" ] }`
        │                     # Each dimension of the label should be either the same as the
        │                     # corresponding dimension of the image, or `1` if that dimension of the label
        │                     # is irrelevant.
        │
        └── original          # Intermediate folders are permitted but not necessary and currently contain no extra metadata.
            │
            └── 0             # Multiscale, labeled image. The name is unimportant but is registered in the "labels" group above.
                ├── zarr.json # Zarr Group which is both a multiscaled image as well as a labeled image.
                │             # Metadata of the related image and as well as display information under the "image-label" key.
                │
                ├── 0         # Each multiscale level is stored as a separate Zarr array, as above, but only integer values
                └── ...       # are supported.
```

### High-content screening

The following specification defines the hierarchy for a high-content screening
dataset. Three groups MUST be defined above the images:

- the group above the images defines the well and MUST implement the [well specification](#well-md).
    All images contained in a well are fields of view of the same well
- the group above the well defines a row of wells
- the group above the well row defines an entire plate i.e. a two-dimensional collection of wells organized in rows and columns.
    It MUST implement the [plate specification](#plate-md)

A well row group SHOULD NOT be present if there are no images in the well row.
A well group SHOULD NOT be present if there are no images in the well.

```text
.
│
└── 5966.zarr                 # One OME-Zarr plate (id=5966)
    ├── zarr.json             # Implements "plate" specification
    ├── A                     # First row of the plate
    │   ├── zarr.json
    │   │
    │   ├── 1                 # First column of row A
    │   │   ├── zarr.json     # Implements "well" specification
    │   │   │
    │   │   ├── 0             # First field of view of well A1
    │   │   │   │
    │   │   │   ├── zarr.json # Implements "multiscales", "omero"
    │   │   │   ├── 0         # Resolution levels          
    │   │   │   ├── ...
    │   │   │   └── labels    # Labels (optional)
    │   │   └── ...           # Other fields of view
    │   └── ...               # Other columns
    └── ...                   # Other rows
```

## OME-Zarr Metadata
(metadata)=

The "OME-Zarr Metadata" contains metadata keys as specified below for discovering certain types of data, especially images.

The OME-Zarr Metadata is stored in the various `zarr.json` files throughout the above array hierarchy.
In this file, the metadata is stored under the namespaced key `ome` in `attributes`.
The version of the OME-Zarr Metadata is denoted as a string in the `version` attribute within the `ome` namespace.

The OME-Zarr Metadata version MUST be consistent within a hierarchy.

```jsonc
{
  // ...
  "attributes": {
    "ome": {
      "version": "0.6.dev3",
      // ...
    }
  }
}
```

### "coordinateSystems" metadata
(coordinate-systems-md)=

A `coordinateSystem` is a JSON object with a `name` field and a `axes` field.
Every coordinate system:
- MUST contain the field `name`.
  The value MUST be a non-empty string that is unique among all entries under `coordinateSystems`.
- MUST contain the field `axes`, whose value is an array of valid `axes` (see below).
The elements of `axes` correspond to the index of each array dimension and coordinates for points in that coordinate system.
For the below example, the `x` dimension is the last dimension.
The "dimensionality" of a coordinate system is indicated by the length of its `axes` array.
The `volume_micrometers` example coordinate system below is three dimensional (3D).

:::{dropdown} Example

Coordinate Systems metadata example

```json
{
    "name" : "volume_micrometers",
    "axes" : [
        {"name": "z", "type": "space", "unit": "micrometer"},
        {"name": "y", "type": "space", "unit": "micrometer"},
        {"name": "x", "type": "space", "unit": "micrometer"}
    ]
}
```
:::

The axes of a coordinate system (see below) give information
about the types, units, and other properties of the coordinate system's dimensions.
Axis names may contain semantically meaningful information, but can be arbitrary.
As a result, two coordinate systems that have identical axes in the same order 
may not be "the same" in the sense that measurements at the same point
refer to different physical entities and therefore should not be analyzed jointly.
Tasks that require images, annotations, regions of interest, etc.,
SHOULD ensure that they are in the same coordinate system (same name and location within the Zarr hierarchy, with identical axes)
or can be transformed to the same coordinate system before doing analysis.
See the [example below](#spec:example:coordinate_transformation).

#### "axes" metadata

`axes` describes the dimensions of a coordinate systems
and adds an interpretation to the samples along that dimension.

It is a list of dictionaries,
where each dictionary describes a dimension (axis) and:
- MUST contain the field `name` that gives the name for this dimension.
  The values MUST be unique across all `name` fields in the same coordinate system.
- SHOULD contain the field `type`.
  It SHOULD be one of the strings `array`, `space`, `time`, `channel`, `coordinate`, or `displacement`
  but MAY take other string values for custom axis types that are not part of this specification yet.
- MAY contain the field `discrete`.
  The value MUST be a boolean,
  and is `true` if the axis represents a discrete dimension (see below for details).
- SHOULD contain the field `unit` to specify the physical unit of this dimension.
  The value SHOULD be one of the following strings,
  which are valid units according to UDUNITS-2.
    - Units for `space` axes: 'angstrom', 'attometer', 'centimeter', 'decimeter', 'exameter', 'femtometer', 'foot', 'gigameter', 'hectometer', 'inch', 'kilometer', 'megameter', 'meter', 'micrometer', 'mile', 'millimeter', 'nanometer', 'parsec', 'petameter', 'picometer', 'terameter', 'yard', 'yoctometer', 'yottameter', 'zeptometer', 'zettameter'
    - Units for `time` axes: 'attosecond', 'centisecond', 'day', 'decisecond', 'exasecond', 'femtosecond', 'gigasecond', 'hectosecond', 'hour', 'kilosecond', 'megasecond', 'microsecond', 'millisecond', 'minute', 'nanosecond', 'petasecond', 'picosecond', 'second', 'terasecond', 'yoctosecond', 'yottasecond', 'zeptosecond', 'zettasecond'
- MAY contain the field `longName`.
  The value MUST be a string,
  and can provide a longer name or description of an axis and its properties.

The length of `axes` MUST be equal to the number of dimensions of the arrays that contain the image data.

Arrays are inherently discrete (see Array coordinate systems, below)
but are often used to store discrete samples of a continuous variable.
The continuous values "in between" discrete samples can be retrieved using an *interpolation* method.
If an axis is continuous (`"discrete" : false`), it indicates that interpolation is well-defined.
Axes representing `space` and `time` are usually continuous.
Similarly, joint interpolation across axes is well-defined only for axes of the same `type`.
In contrast, discrete axes (`"discrete" : true`) may be indexed only by integers.
Axes representing a channel, coordinate, or displacement are usually discrete.

```{note}
The most common methods for interpolation are "nearest neighbor", "linear", "cubic", and "windowed sinc".
Here, we refer to any method that obtains values at real-valued coordinates using discrete samples as an "interpolator".
As such, label images may be interpolated using "nearest neighbor" to obtain labels at points along the continuum.
```

#### Array coordinate systems

The dimensions of an array do not have an interpretation
until they are associated with a coordinate system via a coordinate transformation.
Nevertheless, it can be useful to refer to the "raw" coordinates of the array.
Some applications might prefer to define points or regions-of-interest in "pixel coordinates" rather than "physical coordinates," for example.
Indicating that choice explicitly will be important for interoperability.
This is possible by using **array coordinate systems**.

Every array has a default coordinate system whose parameters need not be explicitly defined.
The dimensionality of each array coordinate system equals the dimensionality of its corresponding Zarr array.
Its name is the path to the array in the container,
its axes have `"type": "array"`, are unitless, and have default names.
The i-th axis has `"name": "dim_i"` (these are the same default names used by [xarray](https://docs.xarray.dev/en/stable/user-guide/terminology.html)).
As with all coordinate systems, the dimension names must be unique and non-null.

:::{dropdown} Example
```json
{
  "arrayCoordinateSystem" : {
    "name" : "myDataArray",
    "axes" : [
      {"name": "dim_0", "type": "array"},
      {"name": "dim_1", "type": "array"},
      {"name": "dim_2", "type": "array"}
    ]
  }
}

```

For example, if 0/zarr.json contains:
```jsonc
{
    "zarr_format": 3,
    "node_type": "array",
    "shape": [4, 3, 5],
    //...
}
```

Then `dim_0` has length 4, `dim_1` has length 3, and `dim_2` has length 5.

:::

The axes and their order align with the shape of the corresponding zarr array,
and whose data depends on the byte order used to store chunks.
As described in the [Zarr array metadata](https://zarr.readthedocs.io/en/stable/spec/v3.html#arrays),
the last dimension of an array in "C" order are stored contiguously on disk or in-memory when directly loaded. 

The name and axes names MAY be customized by including a `arrayCoordinateSystem` field
in the user-defined attributes of the array whose value is a coordinate system object.
The length of `axes` MUST be equal to the dimensionality.
The value of `type` for each object in the axes array MUST equal `"array"`.

#### Coordinate convention

**The pixel/voxel center is the origin of the continuous coordinate system.**

It is vital to consistently define relationship
between the discrete/array and continuous/interpolated coordinate systems.
A pixel/voxel is the continuous region (rectangle) that corresponds to a single sample in the discrete array, i.e.,
the area corresponding to nearest-neighbor (NN) interpolation of that sample.
The center of a 2d pixel corresponding to the origin `(0,0)` in the discrete array
is the origin of the continuous coordinate system `(0.0, 0.0)` (when the transformation is the identity).
The continuous rectangle of the pixel is given
by the half-open interval `[-0.5, 0.5) x [-0.5, 0.5)` (i.e., -0.5 is included, +0.5 is excluded).
See chapter 4 and figure 4.1 of the ITK Software Guide.

### bioformats2raw.layout

(bf2raw)=

[=Transitional=] `"bioformats2raw.layout` metadata identifies a group which implicitly describes a series of images.
The need for the collection stems from the common "multi-image file" scenario in microscopy.
Parsers like Bio-Formats define a strict, stable ordering of the images in a single container that can be used to refer to them by other tools.

In order to capture that information within an OME-Zarr dataset, `bioformats2raw` internally introduced a wrapping layer.
The bioformats2raw layout has been added to v0.4 as a transitional specification to specify filesets that already exist in the wild.
An upcoming NGFF specification will replace this layout with explicit metadata.

#### Layout

(bf2raw-layout)=

Typical Zarr layout produced by running `bioformats2raw` on a fileset that contains more than one image (series > 1):

```text
series.ome.zarr               # One converted fileset from bioformats2raw
    ├── zarr.json             # Contains "bioformats2raw.layout" metadata
    ├── OME                   # Special group for containing OME metadata
    │   ├── zarr.json         # Contains "series" metadata
    │   └── METADATA.ome.xml  # OME-XML file stored within the Zarr fileset
    ├── 0                     # First image in the collection
    ├── 1                     # Second image in the collection
    └── ...
```

#### bf2raw-attributes
(bf2raw-attributes-md)=

The OME-Zarr Metadata in the top-level `zarr.json` file must contain the `bioformats2raw.layout` key:

```{literalinclude} examples/bf2raw/image.json
:language: json
```

If the top-level group represents a plate, the `bioformats2raw.layout` metadata will be present
but the `plate` key MUST also be present, takes precedence and parsing of such datasets should follow (see [plate metadata](#plate-md)).
It is not possible to mix collections of images with plates at present.

```{literalinclude} examples/bf2raw/plate.json
:language: json
```

The OME-Zarr Metadata in the `zarr.json` file within the OME group may contain the `series` key:

```{literalinclude} examples/ome/series-2.json
:language: json
```

#### Details
(bf2raw-details)=

Conforming groups:

- MUST have the value `3` for the `bioformats2raw.layout` key in their OME-Zarr Metadata in the `zarr.json` at the top of the hierarchy;
- SHOULD have OME metadata representing the entire collection of images in a file named `OME/METADATA.ome.xml` which:
  - MUST adhere to the OME-XML specification but
  - MUST use `<MetadataOnly/>` elements as opposed to `<BinData/>`, `<BinaryOnly/>` or `<TiffData/>`;
  - MAY make use of the [minimum specification](https://docs.openmicroscopy.org/ome-model/6.2.2/specifications/minimum.html).

Additionally, the logic for finding the Zarr group for each image follows the following logic:

- If `plate` metadata is present, images MUST be located at the defined location.
  - Matching `series` metadata (as described next) SHOULD be provided for tools that are unaware of the `plate` specification.
- If the `OME` Zarr group exists, it:
  - MAY contain a `series` attribute. If so:
    - `series` MUST be a list of string objects, each of which is a path to an image group.
    - The order of the paths MUST match the order of the `Image` elements in `OME/METADATA.ome.xml` if provided.
- If the `series` attribute does not exist and no `plate` is present:
  - separate `multiscales` images MUST be stored in consecutively numbered groups starting from 0 (i.e. `0/`, `1/`, `2/`, `3/`, ...).
- Every `multiscales` group MUST represent exactly one OME-XML `Image` in the same order as either the series index or the group numbers.
Conforming readers:

- SHOULD make users aware of the presence of more than one image (i.e. SHOULD NOT default to only opening the first image);
- MAY use the `series` attribute in the `OME` group to determine a list of valid groups to display;
- MAY choose to show all images within the collection or offer the user a choice of images, as with <dfn export="true"><abbr title="High-content screening">HCS</abbr></dfn> plates;
- MAY ignore other groups or arrays under the root of the hierarchy.

### "coordinateTransformations" metadata
(coord-trafo-md)=

`coordinateTransformations` describe the mapping between two coordinate systems (defined by [`coordinateSystems`](#coordinate-systems-md)).
For example, to map an array's discrete coordinate system to its corresponding physical coordinates.
Coordinate transforms are in the "forward" direction.
This means they represent functions from *points* in the input space to *points* in the output space
(see [example below](#spec:example:coordinate_transformation_scale)).

They:

- MUST contain the field `type` (string).
- MUST contain any other fields required by the given `type` (see table below).
- MUST contain the field `output` (string),
  unless part of a `sequence` or `inverseOf` (see details).
- MUST contain the field `input` (string),
  unless part of a `sequence` or `inverseOf` (see details).
- MAY contain the field `name` (string).
  Its value MUST be unique across all `name` fields for coordinate transformations.
- Parameter values MUST be compatible with input and output space dimensionality (see details).

The following transformations are supported:

| Type | Fields | Description |
|------|--------|-------------|
| [`identity`](#identity-md) | | The identity transformation is the do-nothing transformation and is typically not explicitly defined. |
| [`mapAxis`](#mapaxis-md) | `"mapAxis":List[number]` | an axis permutation as a transpose array of integer indices that refer to the ordering of the axes in the respective coordinate system. |
| [`translation`](#translation-md) | one of:<br>`"translation":List[number]`,<br>`"path":str` | Translation vector, stored either as a list of numbers (`translation`) or as a zarr array at a location in this container (`path`). |
| [`scale`](#scale-md) | one of:<br>`"scale":List[number]`,<br>`"path":str` | Scale vector, stored either as a list of numbers (`scale`) or as a zarr array at a location in this container (`path`). |
| [`affine`](#affine-md) | one of:<br>`"affine":List[List[number]]`,<br>`"path":str` | 2D affine transformation matrix stored either with JSON (`affine`) or as a zarr array at a location in this container (`path`). |
| [`rotation`](#rotation-md) | one of:<br>`"rotation":List[List[number]]`,<br>`"path":str` | 2D rotation transformation matrix stored as an array stored either with json (`rotation`) or as a zarr array at a location in this container (`path`).|
| [`sequence`](#sequence-md) | `"transformations":List[Transformation]` | sequence of transformations. Applying the sequence applies the composition of all transforms in the list, in order. |
| [`displacements`](#coordinates-displacements-md) | `"path":str`<br>`"interpolation":str` | Displacement field transformation located at `path`. |
| [`coordinates`](#coordinates-displacements-md) | `"path":str`<br>`"interpolation":str` | Coordinate field transformation located at `path`. |
| [`inverseOf`](#inverseof-md) | `"transformation":Transformation` | The inverse of a transformation. Useful if a transform is not closed-form invertible. See forward and inverse of [bijections](#bijection-md) for details and examples. |
| [`bijection`](#bijection-md) | `"forward":Transformation`<br>`"inverse":Transformation` | An invertible transformation providing an explicit forward transformation and its inverse. |
| [`byDimension`](#bydimension-md) | `"transformations":List[Transformation]`, <br> `"input_axes": List[str]`, <br> `"output_axes": List[str]` | A high dimensional transformation using lower dimensional transformations on subsets of dimensions. |

Implementations SHOULD prefer to store transformations as a sequence of less expressive transformations where possible
(e.g., sequence[translation, rotation], instead of affine transformation with translation/rotation). 

:::{dropdown} Example
(spec:example:coordinate_transformation_scale)=

```json
{
  "coordinateSystems": [
    { "name": "in", "axes": [{"name": "j"}, {"name": "i"}] },
    { "name": "out", "axes": [{"name": "y"}, {"name": "x"}] }
  ],
  "coordinateTransformations": [ 
    {
      "type": "scale",
      "scale": [2, 3.12],
      "input": "in",
      "output": "out"
    }
  ]
}

```

For example, the scale transformation above defines the function:

```
x = 3.12 * i
y = 2 * j
```

i.e., the mapping from the first input axis to the first output axis is determined by the first scale parameter.
:::

Conforming readers:
- MUST parse `identity`, `scale`, `translation` transformations;
- SHOULD parse `mapAxis`, `affine`, `rotation` transformations;
- SHOULD display an informative warning if encountering transformations that cannot be parsed or displayed by a viewer;
- SHOULD be able to apply transformations to points;
- SHOULD be able to apply transformations to images;

Coordinate transformations can be stored in multiple places to reflect different usecases.
     
- Transformations in individual multiscale datasets represent a special case of transformations
  and are explained [below](#multiscales-md).
- Additional transformations for single multiscale images MUST be stored under a field `coordinateTransformations`
  in the multiscales dictionaries.
  This `coordinateTransformations` field MUST contain a list of valid [transformations](#trafo-types-md).
- Transformations between two or more images MUST be stored in the attributes of a parent zarr group.
  For transformations that store data or parameters in a zarr array,
  those zarr arrays SHOULD be stored in a zarr group called `coordinateTransformations`.


<pre>
store.zarr                      # Root folder of the zarr store
│
├── zarr.json                   # coordinate transformations describing the relationship between two image coordinate systems
│                               # are stored in the attributes of their parent group.
│                               # transformations between coordinate systems in the 'volume' and 'crop' multiscale images are stored here.
│
├── coordinateTransformations   # transformations that use array storage for their parameters should go in a zarr group named "coordinateTransformations".
│   └── displacements           # for example, a zarr array containing a displacement field
│       └── zarr.json
│
├── volume
│   ├── zarr.json              # group level attributes (multiscales)
│   └── 0                      # a group containing the 0th scale
│       └── image              # a zarr array
│           └── zarr.json      # physical coordinate system and transformations here
└── crop
    ├── zarr.json              # group level attributes (multiscales)
    └── 0                      # a group containing the 0th scale
        └── image              # a zarr array
            └── zarr.json      # physical coordinate system and transformations here
</pre>

:::{dropdown} Example
(spec:example:coordinate_transformation)=
Two instruments simultaneously image the same sample from two different angles,
and the 3D data from both instruments are calibrated to "micrometer" units.
An analysis of sample A requires measurements from images taken from both instruments at certain points in space.
Suppose a region of interest (ROI) is determined from the image obtained from instrument 2,
but quantification from that region is needed for instrument 1.
Since measurements were collected at different angles,
a measurement by instrument 1 at the point with image array coordinates (x,y,z)
may not correspond to the measurement at the same array coordinates in instrument 2
(i.e., it may not be the same physical location in the sample).
To analyze both images together, they must be transformed to a common coordinate system.

The set of coordinate transformations encodes relationships between coordinate systems,
specifically, how to convert points from one coordinate system to another.
Implementations can apply the coordinate transform to images or points
in coordinate system `sampleA_instrument2` to bring them into the `sampleA_instrument1` coordinate system.
In this case, image data within the ROI defined in image2 should be transformed to the `sampleA_instrument1` coordinate system,
then used for quantification with the instrument 1 image.

The `coordinateTransformations` in the parent-level metadata would contain the following data.
The transformation parameters are stored in a separate zarr-group
under `coordinateTransformations/sampleA_instrument2-to-instrument1` as shown above.

```json
"coordinateTransformations": [
    {
        "type": "affine",
        "path": "coordinateTransformations/sampleA_instrument2-to-instrument1",
        "input": "sampleA_instrument2",
        "output": "sampleA_instrument1"
    }
]
```

And the image at the path `sampleA_instrument1` would have the following as the first coordinate system:

```json
"coordinateSystems": [
    {
        "name": "sampleA-instrument1",
        "axes": [
            {"name": "z", "type": "space", "unit": "micrometer"},
            {"name": "y", "type": "space", "unit": "micrometer"},
            {"name": "x", "type": "space", "unit": "micrometer"}
        ]
    },
]
```

The image at path `sampleA_instrument2` would have this as the first listed coordinate system:

```json
[
    {
        "name": "sampleA-instrument2",
        "axes": [
            {"name": "z", "type": "space", "unit": "micrometer"},
            {"name": "y", "type": "space", "unit": "micrometer"},
            {"name": "x", "type": "space", "unit": "micrometer"}
        ]
    }
],
```
:::

#### Additional details

Most coordinate transformations MUST specify their input and output coordinate systems
using `input` and `output` with a string value
that MUST correspond to the name of a coordinate system or the path to a multiscales group.
Exceptions are if the coordinate transformation is wrapped in another transformation,
e.g. as part of a  `transformations` list of a `sequence` or
as `transformation` of an `inverseOf` transformation.
In these two cases input and output could, in some cases, be omitted (see below for details).
If unused, the `input` and `output` fields MAY be null.

If used in a parent-level zarr-group, the `input` and `output` fields
can be the name of a `coordinateSystem` in the same parent-level group or the path to a multiscale image group.
If either `input` or `output` is a path to a multiscale image group,
the authoritative coordinate system for the respective image is the first `coordinateSystem` defined therein.
If the names of `input` or `output` correspond to both an existing path to a multiscale image group
and the name of a `coordinateSystem` defined in the same metadata document,
the `coordinateSystem` MUST take precedent.

For usage in multiscales, see [the multiscales section](#multiscales-md) for details.

Coordinate transformations are functions of *points* in the input space to *points* in the output space.
We call this the "forward" direction.
Points are ordered lists of coordinates,
where a coordinate is the location/value of that point along its corresponding axis.
The indexes of axis dimensions correspond to indexes into transformation parameter arrays.

When rendering transformed images and interpolating,
implementations may need the "inverse" transformation - 
from the output to the input coordinate system.
Inverse transformations will not be explicitly specified
when they can be computed in closed form from the forward transformation.
Inverse transformations used for image rendering may be specified using
the `inverseOf` transformation type, for example:

```json
{
    "type": "inverseOf",
    "transformation" : {
        "type": "displacements",
        "path": "/path/to/displacements",
    },
    "input": "input_image",
    "output": "output_image",
}
```

Implementations SHOULD be able to compute and apply
the inverse of some coordinate transformations when they are computable
in closed-form (as the [Transformation types](#trafo-types-md) section below indicates).
If an operation is requested that requires
the inverse of a transformation that can not be inverted in closed-form,
implementations MAY estimate an inverse,
or MAY output a warning that the requested operation is unsupported.

#### Matrix transformations
(matrix-trafo-md)=

Two transformation types ([affine](#affine-md) and [rotation](#rotation-md)) are parametrized by matrices.
Matrices are applied to column vectors that represent points in the input coordinate system.
The first and last axes in a coordinate system correspond to the top and bottom entries in the column vector, respectively.
Matrices are stored as two-dimensional arrays, either as json or in a zarr array.
When stored as a 2D zarr array, the first dimension indexes rows and the second dimension indexes columns
(e.g., an array of `"shape":[3,4]` has 3 rows and 4 columns).
When stored as a 2D json array, the inner array contains rows (e.g. `[[1,2,3], [4,5,6]]` has 2 rows and 3 columns).

:::{dropdown} Example

For matrix transformations, points in the coordinate system:

```json
{
  "name" : "in",
  "axes" : [
    {"name" : "z"},
    {"name" : "y"},
    {"name":"x"}
  ]
},
```

are represented as column vectors:

```
[z]
[y]
[x]
```

As a result, transforming the point `[z,y,x]=[1,2,3]` with the matrix `[[0,1,0],[-1,0,0],[0,0,-1]]` results in the point `[2,-1,3]`
because it is computed with the matrix-vector multiplication:

```
[ 0  1  0] [1]   [ 2]
[-1  0  0] [2] = [-1]
[ 0  0 -1] [3]   [-3]
```

:::

#### Transformation types
(trafo-types-md)=

Input and output dimensionality may be determined by the coordinate system referred to by the `input` and `output` fields, respectively. 
If the value of `input` is a path to an array, its shape gives the input dimension,
otherwise it is given by the length of `axes` for the coordinate system with the name of the `input`.
If the value of `output` is an array, its shape gives the output dimension,
otherwise it is given by the length of `axes` for the coordinate system with the name of the `output`.

##### identity
(identity-md)=

`identity` transformations map input coordinates to output coordinates without modification.
The position of the i-th axis of the output coordinate system
is set to the position of the ith axis of the input coordinate system.
`identity` transformations are invertible.

The `input` and `output` fields MAY be omitted if wrapped in another transformation that provides `input`/`output`
(e.g., [`sequence`](#sequence-md), [`inverseOf`](#inverseof-md), ['byDimension](#bydimension-md) or [`bijection`](#bijection-md)).

:::{dropdown} Example
:animate: fade-in

```{literalinclude} examples/transformations/identity.json
:language: json
```

defines the function:

```
x = i
y = j
```

:::

##### mapAxis
(mapAxis-md)=

`mapAxis` transformations describe axis permutations as a transpose vector of integers.
Transformations MUST include a `mapAxis` field
whose value is an array of integers that specifies the new ordering in terms of indices of the old order.
The length of the array MUST equal the number of dimensions in both the input and output coordinate systems.
Each integer in the array MUST be a valid zero-based index into the input coordinate system's axes
(i.e., between 0 and N-1 for an N-dimensional input).
Each index MUST appear exactly once in the array.
The value at position `i` in the array indicates which input axis becomes the `i`-th output axis.
`mapAxis` transforms are invertible.

The `input` and `output` fields MAY be omitted if wrapped in another transformation that provides `input`/`output`
(e.g., [`sequence`](#sequence-md), [`inverseOf`](#inverseof-md), ['byDimension](#bydimension-md) or [`bijection`](#bijection-md)).


:::{dropdown} Example 1
:animate: fade-in

```{literalinclude} examples/transformations/mapAxis1.json
:language: json
```

The "equivalent to identity" transformation defines the function:

```
x = i
y = j
```

and the "permutation" transformation defines the function

```
x = j
y = i
```

:::

:::{dropdown} Example 2
:animate: fade-in

```{literalinclude} examples/transformations/mapAxis2.json
:language: json
```

The `projection_down` transformation defines the function:

```
x = b
```

and the `projection_up` transformation defines the function:

```
x = a
y = b
z = b
```
:::

##### translation
(translation-md)=

`translation` transformations are special cases of affine transformations.
When possible, a translation transformation should be preferred to its equivalent affine.
Input and output dimensionality MUST be identical
and MUST equal the the length of the `translation` array (N).
`translation` transformations are invertible.

The `input` and `output` fields MAY be omitted if wrapped in another transformation that provides `input`/`output`
(e.g., [`sequence`](#sequence-md), [`inverseOf`](#inverseof-md), ['byDimension](#bydimension-md) or [`bijection`](#bijection-md)).

<strong>path</strong>
: The path to a zarr-array containing the translation parameters.
The array at this path MUST be 1D, and its length MUST be `N`.

<strong>translation</strong>
: The translation parameters stored as a JSON list of numbers.
The list MUST have length `N`.

:::{dropdown} Example
:animate: fade-in

```{literalinclude} examples/transformations/translation.json
:language: json
```

defines the function:

```
x = i + 9 
y = j - 1.42
```
:::

##### scale
(scale-md)=

`scale` transformations are special cases of affine transformations.
When possible, a scale transformation SHOULD be preferred to its equivalent affine.
Input and output dimensionality MUST be identical
and MUST equal the the length of the `scale` array (N).
Values in the `scale` array SHOULD be non-zero;
in that case, `scale` transformations are invertible.

The `input` and `output` fields MAY be omitted if wrapped in another transformation that provides `input`/`output`
(e.g., [`sequence`](#sequence-md), [`inverseOf`](#inverseof-md), [`byDimension`](#bydimension-md) or [`bijection`](#bijection-md)).

<strong>path</strong>
: The path to a zarr-array containing the scale parameters.
The array at this path MUST be 1D, and its length MUST be `N`.

<strong>scale</strong>
: The scale parameters are stored as a JSON list of numbers.
The list MUST have length `N`.

:::{dropdown} Example 1
:animate: fade-in

```{literalinclude} examples/transformations/scale.json
:language: json
```

defines the function:

```
x = 3.12 * i
y = 2 * j
```
i.e., the mapping from the first input axis to the first output axis is determined by the first scale parameter.

:::

:::{dropdown} Example 2
:animate: fade-in

If the data contains discrete axes (e.g., channels),
these axes are typically not transformed, but must be represented in the scale parameters.

```{literalinclude} examples/transformations/scale_with_discrete.json
:language: json
```
:::

##### affine
(affine-md)=

`affine`s are [matrix transformations](#matrix-trafo-md) from N-dimensional inputs to M-dimensional outputs.
They are represented as the upper `(M)x(N+1)` sub-matrix of a `(M+1)x(N+1)` matrix in [homogeneous
coordinates](https://en.wikipedia.org/wiki/Homogeneous_coordinates) (see examples).
This transformation type may be (but is not necessarily) invertible
when `N` equals `M`.
The matrix MUST be stored as a 2D array either as json or as a zarr array.

The `input` and `output` fields MAY be omitted if wrapped in another transformation that provides `input`/`output`
(e.g., [`sequence`](#sequence-md), [`inverseOf`](#inverseof-md), ['byDimension](#bydimension-md) or [`bijection`](#bijection-md)).

<strong>path</strong>
:  The path to a zarr-array containing the affine parameters.
The array at this path MUST be 2D whose shape MUST be `(M)x(N+1)`.

<strong>affine</strong>
: The affine parameters stored in JSON.
The matrix MUST be stored as 2D nested array (an array of arrays of numbers)
where the outer array MUST be length `M` and the inner arrays MUST be length `N+1`.

:::{dropdown} Example 1
:animate: fade-in
A 2D-2D example:

```{literalinclude} examples/transformations/affine2d2d.json
:language: json
```

defines the function:

```
y = 1*j + 2*i + 3
x = 4*j + 5*i + 6
```

it is equivalent to this matrix-vector multiplication in homogeneous coordinates:

```
[ 1 2 3 ][ j ]   [ y ]
[ 4 5 6 ][ i ] = [ x ]
[ 0 0 1 ][ 1 ]   [ 1 ]
```

where the last row `[0 0 1]` is omitted in the JSON representation.

:::

:::{dropdown} Example 2
:animate: fade-in
An example with two dimensional inputs and three dimensional outputs.
The affine transformation adds a translation by 1 along the new z-axis.

Note that the order of the axes can in general be determined by the application or user.
These axes relate to the memory or on-disk order insofar as the last dimension is contiguous
when the zarr array is c-order (the default for zarr version 2, and the only option for zarr version 3).

```{literalinclude} examples/transformations/affine2d3d.json
:language: json
```

defines the function:

```
z = 0*i + 0*j + 1
y = 3*i + 4*j + 2
x = 6*i + 7*j + 5

```

it is equivalent to this matrix-vector multiplication in homogeneous coordinates:

```
[ 1 0 0 ][ 1 ]   [ z ]
[ 2 3 4 ][ i ] = [ y ]
[ 5 6 7 ][ j ]   [ x ]
[ 0 0 1 ]        [ 1 ]
```

where the last row `[0 0 1]` is omitted in the JSON representation.
:::

:::{dropdown} Example 3
:animate: fade-in

If the image data contains discrete axes (e.g., channels),
these axes are typically not transformed, but must be represented in the transformation matrix.

```{literalinclude} examples/transformations/affine2d2d_with_channel.json
:language: json
```

##### rotation
(rotation-md)=

`rotation`s are [matrix transformations](#matrix-trafo-md) that are special cases of affine transformations.
When possible, a rotation transformation SHOULD be used instead of an equivalent affine.
Input and output dimensionality (N) MUST be identical.
Rotations are stored as `NxN` matrices, see below,
and MUST have determinant equal to one, with orthonormal rows and columns.
The matrix MUST be stored as a 2D array either as json or in a zarr array.
`rotation` transformations are invertible.

The `input` and `output` fields MAY be omitted if wrapped in another transformation that provides `input`/`output`
(e.g., [`sequence`](#sequence-md), [`inverseOf`](#inverseof-md), ['byDimension](#bydimension-md) or [`bijection`](#bijection-md)).

<strong>path</strong>
: The path to an array containing the affine parameters.
The array at this path MUST be 2D whose shape MUST be `N x N`.

<strong>rotation</strong>
: The parameters stored in JSON.
The matrix MUST be stored as a 2D nested array (an array of arrays of numbers) where the outer array MUST be length `N`
and the inner arrays MUST be length `N`.

:::{dropdown} Example
:animate: fade-in
A 2D example

```{literalinclude} examples/transformations/rotation.json
:language: json
```

defines the function:

```
x = 0*i - 1*j
y = 1*i + 0*j
```
:::

##### inverseOf
(inverseOf-md)=

An `inverseOf` transformation contains another transformation (often non-linear),
and indicates that transforming points from output to input coordinate systems
is possible using the contained transformation.
Transforming points from the input to the output coordinate systems
requires the inverse of the contained transformation (if it exists).

The `input` and `output` fields MAY be omitted for `inverseOf` transformations
if those fields may be omitted for the transformation it wraps.

```{note}
Software libraries that perform image registration
often return the transformation from fixed image coordinates to moving image coordinates,
because this "inverse" transformation is most often required
when rendering the transformed moving image.
Results such as this may be enclosed in an `inverseOf` transformation.
This enables the "outer" coordinate transformation to specify the moving image coordinates
as `input` and fixed image coordinates as `output`,
a choice that many users and developers find intuitive.
```

:::{dropdown} Example
:animate: fade-in

```{literalinclude} examples/transformations/inverseOf.json
:language: json
```
:::

##### sequence
(sequence-md)=

A `sequence` transformation consists of an ordered array of coordinate transformations,
and is invertible if every coordinate transform in the array is invertible
(though could be invertible in other cases as well).
To apply a sequence transformation to a point in the input coordinate system,
apply the first transformation in the list of transformations.
Next, apply the second transformation to the result.
Repeat until every transformation has been applied.
The output of the last transformation is the result of the sequence.

A sequence transformation MUST NOT be part of another sequence transformation.
The `input` and `output` fields MUST be included for sequence transformations.

<strong>transformations</strong>
: A non-empty array of transformations.

:::{note}

Considering transformations as functions of points,
if the list contains transformations `[f0, f1, f2]` in that order,
applying this sequence to point `x` is equivalent to:

```
f2(f1(f0(x)))
```

`f0` is applied first, `f1` is applied second, and `f2` is applied last.

:::

:::{dropdown} Example
:animate: fade-in

This sequence:

```{literalinclude} examples/transformations/sequence.json
:language: json
```

describes the function

```
x = (i + 0.1) * 2
y = (j + 0.9) * 3
```

and is invertible.
:::

##### coordinates and displacements
(coordinates-displacements-md)=

`coordinates` and `displacements` transformations store coordinates or displacements in an array
and interpret them as a vector field that defines a transformation.
The arrays must have a dimension corresponding to every axis of the input coordinate system
and one additional dimension to hold components of the vector.
Applying the transformation amounts to looking up the appropriate vector in the array,
interpolating if necessary,
and treating it either as a position directly (`coordinates`)
or a displacement of the input point (`displacements`).

These transformation types refer to an array at location specified by the `path` parameter.
The input and output coordinate systems for these transformations (`input` / `output` coordinate systems)
constrain the array size and the coordinate system metadata for the array (field `coordinateSystem`).

The `input` and `output` fields MAY be omitted if wrapped in another transformation that provides `input`/`output`
(e.g., [`sequence`](#sequence-md), [`inverseOf`](#inverseof-md), [`byDimension`](#bydimension-md) or [`bijection`](#bijection-md)).

* If the input coordinate system has `N` axes,
  the array at location path MUST have `N+1` dimensions
* The field coordinate system MUST contain an axis identical to every axis
  of its input coordinate system in the same order.
* The field coordinate system MUST contain an axis with type `coordinate` or `displacement`, respectively,
  for transformations of type `coordinates` or `displacements`.
    * This SHOULD be the last axis (contiguous on disk when c-order).
* If the output coordinate system has `M` axes,
  the length of the array along the `coordinate`/`displacement` dimension MUST be of length `M`.

The `i`th value of the array along the `coordinate` or `displacement` axis refers to the coordinate or displacement
of the `i`th output axis. See the example below.

`coordinates` and `displacements` transformations are not invertible in general,
but implementations MAY approximate their inverses.
Metadata for these coordinate transforms have the following fields: 

<dl>
  <dt><strong>path</strong></dt>
  <dd>  The location of the coordinate array in this (or another) container.</dd>
  <dt><strong>interpolation</strong></dt>
  <dd>  The <code>interpolation</code> attributes MAY be provided.
        Its value indicates the interpolation to use
        if transforming points not on the array's discrete grid.
        Values could be:
        <ul>
            <li><code>linear</code> (default)</li>
            <li><code>nearest</code></li>
            <li><code>cubic</code></li>
        </ul></dd>
</dl>


For both `coordinates` and `displacements`,
the array data at referred to by `path` MUST define coordinate system
and coordinate transform metadata:

* Every axis name in the `coordinateTransform`'s `input`
  MUST appear in the coordinate system.
* The array dimension corresponding to the `coordinate` or `displacement` axis
  MUST have length equal to the number of dimensions of the `coordinateTransform` `output`
* If the input coordinate system `N` axes,
  then the array data at `path` MUST have `(N + 1)` dimensions.
* SHOULD have a `name` identical to the `name` of the corresponding `coordinateTransform`.

For `coordinates`:

* `coordinateSystem` metadata MUST have exactly one axis with `"type" : "coordinate"`
* the shape of the array along the "coordinate" axis must be exactly `N`

For `displacements`:

* `coordinateSystem` metadata MUST have exactly one axis with `"type" : "displacement"`
* the shape of the array along the "displacement" axis must be exactly `N`
* `input` and `output` MUST have an equal number of dimensions.

:::{dropdown} Example 1
:animate: fade-in
For example, in 1D:
```json
{
    "name" : "a coordinate field transform",
    "type": "coordinates",
    "path" : "i2xCoordinates",
    "input" : "i",
    "output" : "x",
    "interpolation" : "nearest"
}
```

where we assume input spaces `i` and `x` are defined elsewhere.
Example metadata for the array data at path `coordinates` above:

```json
{
  "coordinateSystems" : [
    {
      "name" : "a coordinate field transform",
      "axes" : [
        { "name": "i", "type": "space", "discrete": true },
        { "name": "c", "type": "coordinate", "discrete": true }
      ]
    } 
  ],
  "coordinateTransformations" : [
    {
      "type" : "identity",
      "output" : "a coordinate field transform"
    }
  ]
}
```

If the array in `coordinates` contains the data: `[-9, 9, 0]`, then this metadata defines the function:

```
x = 
    if ( i < 0.5 )                      -9
    else if ( i >= 0.5 and i < 1.5 )     9
    else if ( i >= 1.5 )                 0
```
:::

:::{dropdown} Example 2
:animate: fade-in
A 1D example displacement field:
```json
{
  "name" : "a displacement field transform",
  "type": "displacements",
  "path" : "displacements",
  "input" : "i",
  "output" : "x",
  "interpolation" : "linear"
}
```

where we assume input spaces `i` and `x` are defined elsewhere.
Example metadata for the array data at path `displacements` above:

```json
{
  "coordinateSystems" : [
    {
      "name" : "a displacement field transform",
      "axes" : [
        { "name": "x", "type": "space", "unit" : "nanometer" },
        { "name": "d", "type": "displacement", "discrete": true }
      ]
    } 
  ],
  "coordinateTransformations" : [
    {
      "type" : "scale",
      "scale" : [2, 1],
      "output" : "a displacement field transform"
    }
  ]
}
```

If the array in `displacements` contains the data: `[-1, 0, 1]`,
this transformation maps the point `[1.0]` to the point `[0.5]`.
A scale transformation maps the array coordinates to the `x` axis.
Using the inverse of the scale transform, we see that we need the position `0.5` in array coordinates.
The transformation specifies linear interpolation,
which in this case yields `(0.5 * -1) + (0.5 * 0) = -0.5`.
That value gives us the displacement of the input point,
hence the output is `1.0 + (-0.5) = 0.5`.
:::

:::{dropdown} Example 3
:animate: fade-in

In this example, the array located at `displacementField` MUST have three dimensions.
One dimension MUST correspond to an axis with `type : displacement` (in this example, the last dimension),
the other two dimensions MUST be axes that are identical to the axes of the `in` coordinate system.

```json
"coordinateSystems" : [
  { "name" : "in", "axes" : [{"name" : "y"}, {"name":"x"}] },
  { "name" : "out", "axes" : [{"name" : "y"}, {"name":"x"}] }
],
"coordinateTransformations" : [
  {
    "type": "displacements",
    "input" : "in",
    "output" : "out",
    "path" : "displacementField"
  }
]
```

The metadata at location `displacementField` should have a coordinate system such as:

```json
"coordinateSystems" : [
  { "name" : "in", "axes" : [
    {"name":"y"}, {"name":"x"},
    {"name":"d", "type":"displacement", "discrete":true} ]
  }
]
```

Indexing into this array using c-order, for spatial positions `y` and `x`, the y- and x-displacements would be given by:

```
y_displacement = displacementField[y][x][0]
x_displacement = displacementField[y][x][1]
```

I.e. the y-displacement is first, because the y-axis is the first element of the input and output coordinate systems.

:::

##### byDimension
(byDimension-md)=

`byDimension` transformations build a high dimensional transformation
using lower dimensional transformations on subsets of dimensions.
The `input` and `output` fields MUST always be included for this transformations type.

<dl>
  <dt><strong>transformations</strong></dt>
  <dd>  Each child transformation MUST contain <code>input_axes</code> and <code>output_axes</code> fields
        whose values are arrays of strings.
        Every axis name in a child transformation's <code>input_axes</code>
        MUST correspond to a name of some axis in this parent object's <code>input</code> coordinate system.
        Every axis name in the parent byDimension's <code>output</code> coordinate system
        MUST appear in exactly one child transformation's <code>output_axes</code> array.
        Each child transformation's <code>input_axes</code> and <code>output_axes</code> arrays
        MUST have the same length as that transformation's parameter arrays.
        </dd>
</dl>


:::{dropdown} Example 1
:animate: fade-in

A valid `byDimension` transformation:

```{literalinclude} examples/transformations/byDimension1.json
:language: json
```
:::

:::{dropdown} Example 2
:animate: fade-in

Another valid `byDimension` transformation:

```{literalinclude} examples/transformations/byDimension2.json
:language: json
```
:::

:::{dropdown} Example 3
:animate: fade-in

This is an **invalid** `byDimension` transform:

```{literalinclude} examples/transformations/byDimensionInvalid1.json
:language: json
```

It is invalid for two reasons.
First because input `0` used by the scale transformation is not an axis of the `byDimension` transformation's `input`.
Second, the `x` axis of the `output` does not appear in the `output` of any child transformation.

:::

:::{dropdown} Example 4
:animate: fade-in

Another **invalid** `byDimension` transform:

```{literalinclude} examples/transformations/byDimensionInvalid2.json
:language: json
```

This transformation is invalid because the output axis `x` appears in more than one transformation in the `transformations` list.
:::

##### bijection
(bijection-md)=

A bijection transformation is an invertible transformation in
which both the `forward` and `inverse` transformations are explicitly defined.
Each direction SHOULD be a transformation type that is not closed-form invertible.
Its input and output spaces MUST have equal dimension.
The input and output dimensions for the both the forward and inverse transformations
MUST match bijection's input and output space dimensions.

`input` and `output` fields MAY be omitted for the `forward` and `inverse` transformations,
in which case the `forward` transformation's `input` and `output` are understood to match the bijection's,
and the `inverse` transformation's `input` (`output`) matches the bijection's `output` (`input`),
see the example below.

The `input` and `output` fields MAY be omitted for `bijection` transformations
if the fields may be omitted for both its `forward` and `inverse` transformations

Practically, non-invertible transformations have finite extents,
so bijection transforms should only be expected to be correct / consistent for points that fall within those extents.
It may not be correct for any point of appropriate dimensionality.

:::{dropdown} Example
:animate: fade-in

```{literalinclude} examples/transformations/bijection.json
:language: json
```

the input and output of the `forward` and `inverse` transformations are understood to be:

```{literalinclude} examples/transformations/bijection_verbose.json
:language: json
```
:::

### "multiscales" metadata
(multiscales-md)=

Metadata about an image can be found under the `multiscales` key in the group-level OME-Zarr Metadata.
Here, "image" refers to 2 to 5 dimensional data representing image
or volumetric data with optional time or channel axes.
It is stored in a multiple resolution representation.

`multiscales` contains a list of dictionaries where each entry describes a multiscale image.

Each `multiscales` dictionary MUST contain the field `coordinateSystems`,
whose value is an array containing coordinate system metadata
(see [coordinate systems](#coordinate-systems-md)).
The last entry of this array is the "intrinsic" coordinate system
and MUST contain axis information pertaining to physical coordinates.
It should be used for viewing and processing unless a use case dictates otherwise.
It will generally be a representation of the image in its native physical coordinate system.

The following MUST hold for all coordinate systems inside multiscales metadata.
The length of `axes` must be between 2 and 5
and MUST be equal to the dimensionality of the Zarr arrays storing the image data (see `datasets:path`).
The `axes` MUST contain 2 or 3 entries of `type:space`
and MAY contain one additional entry of `type:time`
and MAY contain one additional entry of `type:channel` or a null / custom type.
In addition, the entries MUST be ordered by `type` where the `time` axis must come first (if present),
followed by the  `channel` or custom axis (if present) and the axes of type `space`.
If there are three spatial axes where two correspond to the image plane (`yx`)
and images are stacked along the other (anisotropic) axis (`z`),
the spatial axes SHOULD be ordered as `zyx`.
Each `multiscales` dictionary MUST contain the field `datasets`,
which is a list of dictionaries describing the arrays storing the individual resolution levels.
Each dictionary in `datasets` MUST contain the field `path`,
whose value is a string containing the path to the Zarr array for this resolution relative to the current Zarr group.
The `path`s MUST be ordered from largest (i.e. highest resolution) to smallest.
Every Zarr array referred to by a `path` MUST have the same number of dimensions
and MUST NOT have more than 5 dimensions.
The number of dimensions and order MUST correspond to number and order of `axes`.

Each dictionary in `datasets` MUST contain the field `coordinateTransformations`,
whose value is a list of dictionaries that define a transformation
that maps Zarr array coordinates for this resolution level to the "intrinsic" coordinate system
(the last entry of the `coordinateSystems` array).
The transformation is defined according to [transformations metadata](#trafo-types-md).
The transformation MUST take as input points in the array coordinate system
corresponding to the Zarr array at location `path`.
The value of `input` MUST equal the value of `path`, 
implementations should always treat the value of `input` as if it were equal to the value of `path`.
The value of the transformation’s `output` MUST be the name of the "intrinsic" [coordinate system](#coordinate-systems-md).

This transformation MUST be one of the following:

* A single scale or identity transformation
* A sequence transformation containing one scale and one translation transformation.

In these cases, the scale transformation specifies the pixel size in physical units or time duration.
If scaling information is not available or applicable for one of the axes,
the value MUST express the scaling factor between the current resolution
and the first resolution for the given axis,
defaulting to 1.0 if there is no downsampling along the axis.
This is strongly recommended
so that the the "intrinsic" coordinate system of the image avoids more complex transformations.

If applications require additional transformations,
each `multiscales` dictionary MAY contain the field `coordinateTransformations`,
describing transformations that are applied to all resolution levels in the same manner.
The value of `input` MUST equal the name of the "intrinsic" coordinate system.
The value of `output` MUST be the name of the output coordinate System
which is different from the "intrinsic" coordinate system.

Each `multiscales` dictionary SHOULD contain the field `name`.

Each `multiscales` dictionary SHOULD contain the field `type`,
which gives the type of downscaling method used to generate the multiscale image pyramid.
It SHOULD contain the field `metadata`,
which contains a dictionary with additional information about the downscaling method.


:::{dropdown} Example
:animate: fade-in

A complete example of json-file for a 5D (TCZYX) multiscales with 3 resolution levels could look like this:
```{literalinclude} examples/multiscales_strict/multiscales_example.json
:language: json
```
:::

If only one multiscale is provided, use it.
Otherwise, the user can choose by name,
using the first multiscale as a fallback:

```python
datasets = []
for named in multiscales:
    if named["name"] == "3D":
        datasets = [x["path"] for x in named["datasets"]]
        break
if not datasets:
    # Use the first by default. Or perhaps choose based on chunk size.
    datasets = [x["path"] for x in multiscales[0]["datasets"]]
```

### "omero" metadata (transitional)
(omero-md)=

[=Transitional=] information specific to the channels of an image and how to render it can be found under the `omero` key in the group-level metadata:

```json
"id": 1,                              # ID in OMERO
"name": "example.tif",                # Name as shown in the UI
"channels": [                         # Array matching the c dimension size
    {
        "active": true,
        "coefficient": 1,
        "color": "0000FF",
        "family": "linear",
        "inverted": false,
        "label": "LaminB1",
        "window": {
            "end": 1500,
            "max": 65535,
            "min": 0,
            "start": 0
        }
    }
],
"rdefs": {
    "defaultT": 0,                    # First timepoint to show the user
    "defaultZ": 118,                  # First Z section to show the user
    "model": "color"                  # "color" or "greyscale"
}
```

See the [OMERO WebGateway documentation](https://omero.readthedocs.io/en/stable/developers/Web/WebGateway.html#imgdata)
for more information.

The `omero` metadata is optional, but if present it MUST contain the field `channels`,
which is an array of dictionaries describing the channels of the image.
Each dictionary in `channels` MUST contain the field `color`,
which is a string of 6 hexadecimal digits specifying the color of the channel in RGB format.
Each dictionary in `channels` MUST contain the field `window`,
which is a dictionary describing the windowing of the channel.
The field `window` MUST contain the fields `min` and `max`,
which are the minimum and maximum values of the window, respectively.
It MUST also contain the fields `start` and `end`,
which are the start and end values of the window, respectively.

### "labels" metadata
(labels-md)=

In OME-Zarr, Zarr arrays representing pixel-annotation data are stored in a group called `labels`.
Some applications--notably image segmentation--produce a new image that is in the same coordinate system as a corresponding multiscale image
(usually having the same dimensions and coordinate transformations).
This new image is composed of integer values corresponding to certain labels with custom meanings.
For example, pixels take the value 1 or 0 if the corresponding pixel in the original image represents cellular space or intercellular space, respectively.
Such an image is referred to in this specification as a "label image".

The `labels` group is nested within an image group, at the same level of the Zarr hierarchy as the resolution levels for the original image.
The `labels` group is not itself an image; it contains images.
The pixels of the label images MUST be integer data types,
i.e. one of [`uint8`, `int8`, `uint16`, `int16`, `uint32`, `int32`, `uint64`, `int64`].
Intermediate groups between `labels` and the images within it are allowed,
but these MUST NOT contain metadata.
Names of the images in the `labels` group are arbitrary.

The OME-Zarr Metadata in the `zarr.json` file associated with the `labels` group MUST contain a JSON object with the key `labels`,
whose value is a JSON array of paths to the labeled multiscale image(s).
All label images SHOULD be listed within this metadata file.

:::{dropdown} Example
For example:
```json
{
  "attributes": {
    "ome": {
      "version": "0.6.dev3",
      "labels": [
        "cell_space_segmentation"
      ]
    }
  }
}
```
:::

The `zarr.json` file for the label image MUST implement the multiscales specification.
Within the `multiscales` object, the JSON array associated with the `datasets` key MUST have the same number of entries (scale levels) as the original unlabeled image.

In addition to the `multiscales` key, the OME-Zarr Metadata in this image-level `zarr.json` file SHOULD contain another key, `image-label`,
whose value is also a JSON object.
The `image-label` object stores information about the display colors, source image,
and optionally, further arbitrary properties of the label image.
That `image-label` object SHOULD contain the following keys: first, a `colors` key,
whose value MUST be a JSON array describing color information for the unique label values.
Second, a `version` key, whose value MUST be a string specifying the version of the OME-Zarr `image-label` schema.

Conforming readers SHOULD display labels using the colors specified by the `colors` JSON array, as follows.
This array contains one JSON object for each unique custom label.
Each of these objects MUST contain the `label-value` key, whose value MUST be the integer corresponding to a particular label.
In addition to the `label-value` key, the objects in this array MAY contain an `rgba` key
whose value MUST be an array of four integers between 0 and 255, inclusive.
These integers represent the `uint8` values of red, green, and blue that comprise the final color to be displayed at the pixels with this label.
The fourth integer in the `rgba` array represents alpha, or the opacity of the color.
Additional keys under `colors` are allowed.

Next, the `image-label` object MAY contain the following keys: a `properties` key, and a `source` key.

Like the `colors` key, the value of the `properties` key MUST be an array of JSON objects describing the set of unique possible pixel values.
Each object in the `properties` array MUST contain the `label-value` key,
whose value again MUST be an integer specifying the pixel value for that label.
Additionally, an arbitrary number of key-value pairs MAY be present for each label value,
denoting arbitrary metadata associated with that label.
Label-value objects within the `properties` array do not need to have the same keys.

The value of the `source` key MUST be a JSON object containing information about the original image from which the label image derives.
This object MAY include a key `image`, whose value MUST be a string specifying the relative path to a Zarr image group.  
The default value is `../../` since most labeled images are stored in a "labels" group that is nested within the original image group.


:::{dropdown} Example
Here is an example of a simple `image-label` object for a label image in which 0s and 1s represent intercellular and cellular space, respectively:
```{literalinclude} examples/label_strict/colors_properties.json
:language: json
```
In this case, the pixels consisting of a 0 in the Zarr array will be displayed as 50% blue and 50% opacity.
Pixels with a 1 in the Zarr array, which correspond to cellular space, will be displayed as 50% green and 50% opacity.
:::


### "plate" metadata
(plate-md)=

For high-content screening datasets,
the plate layout can be found under the custom attributes of the plate group under the `plate` key in the group-level metadata.

The `plate` dictionary MAY contain an `acquisitions` key
whose value MUST be a list of JSON objects defining the acquisitions for a given plate to which wells can refer to.
Each acquisition object MUST contain an `id` key
whose value MUST be an unique integer identifier greater than or equal to 0 within the context of the plate
to which fields of view can refer to (see [well metadata](#well-md)).
Each acquisition object SHOULD contain a `name` key whose value MUST be a string
identifying the name of the acquisition.
Each acquisition object SHOULD contain a `maximumfieldcount` key
whose value MUST be a positive integer indicating the maximum number of fields of view for the acquisition.
Each acquisition object MAY contain a `description` key
whose value MUST be a string specifying a description for the acquisition.
Each acquisition object MAY contain a `starttime` and/or `endtime` key
whose values MUST be integer epoch timestamps specifying the start and/or end timestamp of the acquisition.

The `plate` dictionary MUST contain a `columns` key
whose value MUST be a list of JSON objects defining the columns of the plate.
Each column object defines the properties of the column at the index of the object in the list.
Each column in the physical plate MUST be defined,
even if no wells in the column are defined.
Each column object MUST contain a `name` key whose value is a string specifying the column name.
The `name` MUST contain only alphanumeric characters,
MUST be case-sensitive,
and MUST NOT be a duplicate of any other `name` in the `columns` list.
Care SHOULD be taken to avoid collisions on case-insensitive filesystems
(e.g. avoid using both `Aa` and `aA`).

The `plate` dictionary SHOULD contain a `field_count` key
whose value MUST be a positive integer defining the maximum number of fields per view across all wells.

The `plate` dictionary SHOULD contain a `name` key
whose value MUST be a string defining the name of the plate.

The `plate` dictionary MUST contain a `rows` key
whose value MUST be a list of JSON objects defining the rows of the plate.
Each row object defines the properties of the row at the index of the object in the list.
Each row in the physical plate MUST be defined,
even if no wells in the row are defined.
Each defined row MUST contain a `name` key whose value MUST be a string defining the row name.
The `name` MUST contain only alphanumeric characters,
MUST be case-sensitive,
and MUST NOT be a duplicate of any other `name` in the `rows` list.
Care SHOULD be taken to avoid collisions on case-insensitive filesystems
(e.g. avoid using both `Aa` and `aA`).

The `plate` dictionary MUST contain a `version` key
whose value MUST be a string specifying the version of the plate specification.

The `plate` dictionary MUST contain a `wells` key
whose value MUST be a list of JSON objects defining the wells of the plate.
Each well object MUST contain a `path` key
whose value MUST be a string specifying the path to the well subgroup.
The `path` MUST consist of a `name` in the `rows` list,
a file separator (`/`),
and a `name` from the `columns` list,
in that order.
The `path` MUST NOT contain additional leading or trailing directories.
Each well object MUST contain both a `rowIndex` key
whose value MUST be an integer identifying the index into the `rows` list,
and a `columnIndex` key
whose value MUST be an integer identifying the index into the `columns` list.
`rowIndex` and `columnIndex` MUST be 0-based.
The `rowIndex`, `columnIndex`, and `path` MUST all refer to the same row/column pair.

:::{dropdown} Example
For example the following JSON object defines a plate with two acquisitions and 6 wells (2 rows and 3 columns),
containing up to 2 fields of view per acquisition.

```{literalinclude} examples/plate_strict/plate_6wells.json
:language: json
```

The following JSON object defines a sparse plate with one acquisition and 2 wells in a 96 well plate,
containing one field of view per acquisition.

```{literalinclude} examples/plate_strict/plate_2wells.json
:language: json
```
:::

### "well" metadata
(well-md)=

For high-content screening datasets,
the metadata about all fields of views under a given well can be found under the `well` key in the attributes of the well group.

The `well` dictionary MUST contain an `images` key
whose value MUST be a list of JSON objects specifying all fields of views for a given well.
Each image object MUST contain a `path` key
whose value MUST be a string specifying the path to the field of view.
The `path` MUST be case-sensitive, and MUST NOT be a duplicate of any other `path` in the `images` list.
The `path` MUST follow [Zarr node name naming conventions](https://github.com/zarr-developers/zarr-specs/blob/main/docs/v3/core/index.rst#node-names) including the recommended limitations of characters to ensure consistency across different storage systems and programming languages. 
Specifically: The `path` MUST NOT only be composed of periods like `.` or `..` or start with the reserved prefix `__`; 
The `path` MUST NOT be an empty string and MUST NOT contain `/` characters; 
The `path` MUST only use characters in the sets `a-z`, `A-Z`, `0-9`, `-`, `_`, `.`. 
If multiple acquisitions were performed in the plate,
it MUST contain an `acquisition` key whose value MUST be an integer identifying the acquisition
which MUST match one of the acquisition JSON objects defined in the [plate metadata](#plate-md).

The `well` dictionary SHOULD contain a `version` key
whose value MUST be a string specifying the version of the well specification.

:::{dropdown} Example
For example the following JSON object defines a well with four fields of view.
The first two fields of view were part of the first acquisition
while the last two fields of view were part of the second acquisition.

```{literalinclude} examples/well_strict/well_4fields.json
:language: json
```

The following JSON object defines a well with two fields of view in a plate with four acquisitions.
The first field is part of the first acquisition, and the second field is part of the last acquisition.

```{literalinclude} examples/well_strict/well_2fields.json
:language: json
```
:::

## Specification naming style
(naming-style)=

Multi-word keys in this specification should use the `camelCase` style.
NB: some parts of the specification don't obey this convention as they were added before this was adopted,
but they should be updated in due course.

## Implementations
(implementations-md)=

See [Tools](https://ngff.openmicroscopy.org/tools/index.html).
