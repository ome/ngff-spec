# OME-Zarr plate schema

**Title:** OME-Zarr plate schema

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** The zarr.json attributes key

| Property       | Pattern | Type   | Deprecated | Definition | Title/Description                         |
| -------------- | ------- | ------ | ---------- | ---------- | ----------------------------------------- |
| + [ome](#ome ) | No      | object | No         | -          | The versioned OME-Zarr Metadata namespace |

## <a name="ome"></a>1. Property `OME-Zarr plate schema > ome`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

**Description:** The versioned OME-Zarr Metadata namespace

| Property                   | Pattern | Type   | Deprecated | Definition                                                          | Title/Description                                                                                             |
| -------------------------- | ------- | ------ | ---------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| + [plate](#ome_plate )     | No      | object | No         | -                                                                   | -                                                                                                             |
| + [version](#ome_version ) | No      | object | No         | In https://ngff.openmicroscopy.org/0.6.dev1/schemas/_version.schema | 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️ |

### <a name="ome_plate"></a>1.1. Property `OME-Zarr plate schema > ome > plate`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                   | Pattern | Type            | Deprecated | Definition | Title/Description                                      |
| ------------------------------------------ | ------- | --------------- | ---------- | ---------- | ------------------------------------------------------ |
| - [acquisitions](#ome_plate_acquisitions ) | No      | array of object | No         | -          | The acquisitions for this plate                        |
| - [field_count](#ome_plate_field_count )   | No      | integer         | No         | -          | The maximum number of fields per view across all wells |
| - [name](#ome_plate_name )                 | No      | string          | No         | -          | The name of the plate                                  |
| + [columns](#ome_plate_columns )           | No      | array of object | No         | -          | The columns of the plate                               |
| + [rows](#ome_plate_rows )                 | No      | array of object | No         | -          | The rows of the plate                                  |
| + [wells](#ome_plate_wells )               | No      | array of object | No         | -          | The wells of the plate                                 |

#### <a name="ome_plate_acquisitions"></a>1.1.1. Property `OME-Zarr plate schema > ome > plate > acquisitions`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | No                |

**Description:** The acquisitions for this plate

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                     | Description |
| --------------------------------------------------- | ----------- |
| [acquisitions items](#ome_plate_acquisitions_items) | -           |

##### <a name="autogenerated_heading_2"></a>1.1.1.1. OME-Zarr plate schema > ome > plate > acquisitions > acquisitions items

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                                                | Pattern | Type    | Deprecated | Definition | Title/Description                                                                                       |
| ----------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ------------------------------------------------------------------------------------------------------- |
| + [id](#ome_plate_acquisitions_items_id )                               | No      | integer | No         | -          | A unique identifier within the context of the plate                                                     |
| - [maximumfieldcount](#ome_plate_acquisitions_items_maximumfieldcount ) | No      | integer | No         | -          | The maximum number of fields of view for the acquisition                                                |
| - [name](#ome_plate_acquisitions_items_name )                           | No      | string  | No         | -          | The name of the acquisition                                                                             |
| - [description](#ome_plate_acquisitions_items_description )             | No      | string  | No         | -          | The description of the acquisition                                                                      |
| - [starttime](#ome_plate_acquisitions_items_starttime )                 | No      | integer | No         | -          | The start timestamp of the acquisition, expressed as epoch time i.e. the number seconds since the Epoch |
| - [endtime](#ome_plate_acquisitions_items_endtime )                     | No      | integer | No         | -          | The end timestamp of the acquisition, expressed as epoch time i.e. the number seconds since the Epoch   |

###### <a name="ome_plate_acquisitions_items_id"></a>1.1.1.1.1. Property `OME-Zarr plate schema > ome > plate > acquisitions > acquisitions items > id`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

**Description:** A unique identifier within the context of the plate

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

###### <a name="ome_plate_acquisitions_items_maximumfieldcount"></a>1.1.1.1.2. Property `OME-Zarr plate schema > ome > plate > acquisitions > acquisitions items > maximumfieldcount`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

**Description:** The maximum number of fields of view for the acquisition

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &gt; 0 |

###### <a name="ome_plate_acquisitions_items_name"></a>1.1.1.1.3. Property `OME-Zarr plate schema > ome > plate > acquisitions > acquisitions items > name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** The name of the acquisition

###### <a name="ome_plate_acquisitions_items_description"></a>1.1.1.1.4. Property `OME-Zarr plate schema > ome > plate > acquisitions > acquisitions items > description`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** The description of the acquisition

###### <a name="ome_plate_acquisitions_items_starttime"></a>1.1.1.1.5. Property `OME-Zarr plate schema > ome > plate > acquisitions > acquisitions items > starttime`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

**Description:** The start timestamp of the acquisition, expressed as epoch time i.e. the number seconds since the Epoch

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

###### <a name="ome_plate_acquisitions_items_endtime"></a>1.1.1.1.6. Property `OME-Zarr plate schema > ome > plate > acquisitions > acquisitions items > endtime`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

**Description:** The end timestamp of the acquisition, expressed as epoch time i.e. the number seconds since the Epoch

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

#### <a name="ome_plate_field_count"></a>1.1.2. Property `OME-Zarr plate schema > ome > plate > field_count`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | No        |

**Description:** The maximum number of fields per view across all wells

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &gt; 0 |

#### <a name="ome_plate_name"></a>1.1.3. Property `OME-Zarr plate schema > ome > plate > name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** The name of the plate

#### <a name="ome_plate_columns"></a>1.1.4. Property `OME-Zarr plate schema > ome > plate > columns`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

**Description:** The columns of the plate

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 1                  |
| **Max items**        | N/A                |
| **Items unicity**    | True               |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be           | Description |
| ----------------------------------------- | ----------- |
| [columns items](#ome_plate_columns_items) | -           |

##### <a name="autogenerated_heading_3"></a>1.1.4.1. OME-Zarr plate schema > ome > plate > columns > columns items

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| + [name](#ome_plate_columns_items_name ) | No      | string | No         | -          | The column name   |

###### <a name="ome_plate_columns_items_name"></a>1.1.4.1.1. Property `OME-Zarr plate schema > ome > plate > columns > columns items > name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The column name

| Restrictions                      |                                                                                   |
| --------------------------------- | --------------------------------------------------------------------------------- |
| **Must match regular expression** | ```^[A-Za-z0-9]+$``` [Test](https://regex101.com/?regex=%5E%5BA-Za-z0-9%5D%2B%24) |

#### <a name="ome_plate_rows"></a>1.1.5. Property `OME-Zarr plate schema > ome > plate > rows`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

**Description:** The rows of the plate

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 1                  |
| **Max items**        | N/A                |
| **Items unicity**    | True               |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be     | Description |
| ----------------------------------- | ----------- |
| [rows items](#ome_plate_rows_items) | -           |

##### <a name="autogenerated_heading_4"></a>1.1.5.1. OME-Zarr plate schema > ome > plate > rows > rows items

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                              | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| + [name](#ome_plate_rows_items_name ) | No      | string | No         | -          | The row name      |

###### <a name="ome_plate_rows_items_name"></a>1.1.5.1.1. Property `OME-Zarr plate schema > ome > plate > rows > rows items > name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The row name

| Restrictions                      |                                                                                   |
| --------------------------------- | --------------------------------------------------------------------------------- |
| **Must match regular expression** | ```^[A-Za-z0-9]+$``` [Test](https://regex101.com/?regex=%5E%5BA-Za-z0-9%5D%2B%24) |

#### <a name="ome_plate_wells"></a>1.1.6. Property `OME-Zarr plate schema > ome > plate > wells`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

**Description:** The wells of the plate

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | 1                  |
| **Max items**        | N/A                |
| **Items unicity**    | True               |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be       | Description |
| ------------------------------------- | ----------- |
| [wells items](#ome_plate_wells_items) | -           |

##### <a name="autogenerated_heading_5"></a>1.1.6.1. OME-Zarr plate schema > ome > plate > wells > wells items

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | No                                                                        |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |

| Property                                             | Pattern | Type    | Deprecated | Definition | Title/Description                         |
| ---------------------------------------------------- | ------- | ------- | ---------- | ---------- | ----------------------------------------- |
| + [path](#ome_plate_wells_items_path )               | No      | string  | No         | -          | The path to the well subgroup             |
| + [rowIndex](#ome_plate_wells_items_rowIndex )       | No      | integer | No         | -          | The index of the well in the rows list    |
| + [columnIndex](#ome_plate_wells_items_columnIndex ) | No      | integer | No         | -          | The index of the well in the columns list |

###### <a name="ome_plate_wells_items_path"></a>1.1.6.1.1. Property `OME-Zarr plate schema > ome > plate > wells > wells items > path`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The path to the well subgroup

| Restrictions                      |                                                                                                                     |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Must match regular expression** | ```^[A-Za-z0-9]+/[A-Za-z0-9]+$``` [Test](https://regex101.com/?regex=%5E%5BA-Za-z0-9%5D%2B%2F%5BA-Za-z0-9%5D%2B%24) |

###### <a name="ome_plate_wells_items_rowIndex"></a>1.1.6.1.2. Property `OME-Zarr plate schema > ome > plate > wells > wells items > rowIndex`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

**Description:** The index of the well in the rows list

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

###### <a name="ome_plate_wells_items_columnIndex"></a>1.1.6.1.3. Property `OME-Zarr plate schema > ome > plate > wells > wells items > columnIndex`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

**Description:** The index of the well in the columns list

| Restrictions |        |
| ------------ | ------ |
| **Minimum**  | &ge; 0 |

### <a name="ome_version"></a>1.2. Property `OME-Zarr plate schema > ome > version`

|                           |                                                                           |
| ------------------------- | ------------------------------------------------------------------------- |
| **Type**                  | `object`                                                                  |
| **Required**              | Yes                                                                       |
| **Additional properties** | [[Any type: allowed]](# "Additional Properties of any type are allowed.") |
| **Defined in**            | https://ngff.openmicroscopy.org/0.6.dev1/schemas/_version.schema          |

**Description:** 😅 ERROR in schema generation, a referenced schema could not be loaded, no documentation here unfortunately 🏜️

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2025-10-08 at 23:35:16 +0200
