# OME-Zarr container produced by bioformats2raw

**Title:** OME-Zarr container produced by bioformats2raw

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** The zarr.json attributes key

| Property       | Pattern | Type   | Deprecated | Definition | Title/Description                         |
| -------------- | ------- | ------ | ---------- | ---------- | ----------------------------------------- |
| + [ome](#ome ) | No      | object | No         | -          | The versioned OME-Zarr Metadata namespace |

## <a name="ome"></a>1. Property `OME-Zarr container produced by bioformats2raw > ome`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** The versioned OME-Zarr Metadata namespace

| Property                                              | Pattern | Type              | Deprecated | Definition                                                          | Title/Description                                                                                             |
| ----------------------------------------------------- | ------- | ----------------- | ---------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| + [bioformats2raw.layout](#ome_bioformats2rawlayout ) | No      | enum (of integer) | No         | -                                                                   | The top-level identifier metadata added by bioformats2raw                                                     |
| + [version](#ome_version )                            | No      | object            | No         | In https://ngff.openmicroscopy.org/0.6.dev1/schemas/_version.schema | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

### <a name="ome_bioformats2rawlayout"></a>1.1. Property `OME-Zarr container produced by bioformats2raw > ome > bioformats2raw.layout`

|              |                     |
| ------------ | ------------------- |
| **Type**     | `enum (of integer)` |
| **Required** | Yes                 |

**Description:** The top-level identifier metadata added by bioformats2raw

Must be one of:
* 3

### <a name="ome_version"></a>1.2. Property `OME-Zarr container produced by bioformats2raw > ome > version`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | https://ngff.openmicroscopy.org/0.6.dev1/schemas/_version.schema          |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2025-10-08 at 23:34:14 +0200
