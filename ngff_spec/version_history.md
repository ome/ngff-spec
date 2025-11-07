---
author: ""
---
# Version History
(history)=

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.5.2] - 2025-01-10

### Changed

- Clarify that the `dimension_names` field in `axes` MUST be included.

## [0.5.1] - 2025-01-10

### Added

- Re-add the improved omero description in PR-191.

## [0.5.0] - 2024-11-21

### Changed

- use Zarr v3 in OME-Zarr, see [RFC-2](https://ngff.openmicroscopy.org/rfc/2).

## [0.4.1] - 2023-02-09

### Changed

- expand on "labels" description

## [0.4.1] - 2022-09-26

### Added

- transitional metadata for image collections ("bioformats2raw.layout")

## [0.4.0] - 2022-02-08

### Added

- multiscales: add axes type, units and coordinateTransformations
- plate: add rowIndex/columnIndex

## [0.3.0] - 2021-08-24

### Added

- Add axes field to multiscale metadata

## [0.2.0] - 2021-03-29

### Changed

- Change chunk dimension separator to "/"

## [0.1.4] - 2020-11-26

### Added

- Add HCS specification

## [0.1.3] - 2020-09-14

### Added

- Add labels specification

## [0.1.2] - 2020-05-07

### Added

- Add description of "omero" metadata

## [0.1.1] - 2020-05-06

### Added

- Add info on the ordering of resolutions

## [0.1.0] - 2020-04-20

First version for internal demo
