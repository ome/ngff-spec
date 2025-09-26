# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Coordinate systems

### Changed

- `coordinateTransformations` metadata

## [0.5.2] - 2025-01-10

### Changed

- Clarified that the `dimension_names` field in `axes` MUST be included

## [0.5.1] - 2025-01-10

### Fixed

- Re-added the improved omero description from PR-191

## [0.5.0] - 2024-11-21

### Changed

- Use Zarr v3 in OME-Zarr (see [RFC-2](https://ngff.openmicroscopy.org/rfc/2))

## [0.4.2] - 2023-02-09

### Changed

- Expanded "labels" description

## [0.4.1] - 2022-09-26

### Added

- Transitional metadata for image collections ("bioformats2raw.layout")

## [0.4.0] - 2022-02-08

### Added

- multiscales: axes type, units and coordinateTransformations
- plate: rowIndex/columnIndex

## [0.3.0] - 2021-08-24

### Added

- Axes field to multiscale metadata

## [0.2.0] - 2021-03-29

### Changed

- Chunk dimension separator to "/"

## [0.1.4] - 2020-11-26

### Added

- HCS specification

## [0.1.3] - 2020-09-14

### Added

- Labels specification

## [0.1.2] - 2020-05-07

### Added

- Description of "omero" metadata

## [0.1.1] - 2020-05-06

### Added

- Information on the ordering of resolutions

## [0.1.0] - 2020-04-20

### Added

- First version for internal demo
