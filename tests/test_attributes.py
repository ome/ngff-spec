from pathlib import Path
from typing import Any
import json

import pytest

from jsonschema import RefResolver, Draft202012Validator as Validator
from jsonschema.exceptions import ValidationError

here = Path(__file__).resolve().parent
schema_dir = here.parent.joinpath("schemas")
attrs_dir = here / "attributes"

schema_store = {}
version = None
for schema_path in schema_dir.glob("*.schema*"):
    schema = json.loads(schema_path.read_text())
    schema_store[schema["$id"]] = schema
    if schema_path.stem == "_version":
        version = schema["enum"][0]

assert version is not None

GENERIC_SCHEMA = schema_store[
    f"https://ngff.openmicroscopy.org/{version}/schemas/ome_zarr.schema"
]
STRICT_SCHEMA = schema_store[
    f"https://ngff.openmicroscopy.org/{version}/schemas/strict_ome_zarr.schema"
]

case_fnames = sorted(attrs_dir.rglob("*.json"))

xfails = set()


def fname_to_id(fpath: Path) -> str:
    return str(fpath.relative_to(attrs_dir).with_suffix(""))


@pytest.mark.parametrize("case_fname", case_fnames, ids=fname_to_id)
def test_attributes(case_fname: Path):
    if fname_to_id(case_fname) in xfails:
        pytest.xfail("known JSON Schema limitation")

    case_obj: dict[str, Any] = json.loads(case_fname.read_text())

    conformance = case_obj.get("_conformance", {})
    valid = conformance.get("valid", True)
    strict = conformance.get("strict", False)

    if strict:
        schema = STRICT_SCHEMA
    else:
        schema = GENERIC_SCHEMA

    resolver = RefResolver.from_schema(
        schema,
        store=schema_store,
    )

    validator_cls = Validator

    validator = validator_cls(
        schema,
        resolver=resolver,
    )

    if valid:
        validator.validate(case_obj)
    else:
        with pytest.raises(ValidationError):
            validator.validate(case_obj)


if __name__ == '__main__':
    pytest.main([__file__])