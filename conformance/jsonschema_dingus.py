#!/usr/bin/env python3
# /// script
# dependencies = [
#   "jsonschema",
#   "referencing",
# ]
# ///
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json
from argparse import ArgumentParser
from typing import Any, Self

from referencing import Registry, Resource
from jsonschema import Draft202012Validator as Validator
from jsonschema.exceptions import ValidationError

HERE = Path(__file__).resolve().parent
SCHEMA_DIR = HERE / "ngff_spec" / "schemas"


@dataclass
class SchemasInfo:
    generic_id: str
    base_url: str
    registry: Registry

    @classmethod
    def load(cls) -> Self:
        """Get the ID of the top-level schema, and the mapping of schema IDs to objects"""
        registry = Registry()
        generic = None
        base_url = None
        for p in SCHEMA_DIR.glob("*.schema*"):
            schema = json.loads(p.read_text())
            resource = Resource.from_contents(schema)
            registry = resource @ registry

            schema_id = resource.id()
            if schema_id is None:
                raise RuntimeError("schema has no ID")
            if p.stem == "ome_zarr":
                generic = schema_id
                base_url = generic.split("/schemas/")[0]

        if generic is None or base_url is None:
            raise RuntimeError("Could not find generic ome_zarr schema")

        return cls(generic, base_url, registry)


def main(raw_args=None):
    parser = ArgumentParser()
    parser.add_argument("mode", choices=["attributes", "zarr"])
    parser.add_argument("path", type=Path)

    args = parser.parse_args(raw_args)

    p: Path = args.path
    attrs: None | dict[str, Any] = None
    match args.mode:
        case "attributes":
            attrs = json.loads(p.read_text())
        case "zarr":
            attrs = json.loads(p.joinpath("zarr.json").read_text())["attributes"]
        case _:
            raise RuntimeError("unreachable")

    if attrs is None:
        raise RuntimeError("unreachable")

    schemas = SchemasInfo.load()

    generic_schema = schemas.registry.get(schemas.generic_id)
    if generic_schema is None:
        raise RuntimeError("could not find generic schema")

    validator = Validator(
        generic_schema.contents,
        registry=schemas.registry,
    )

    result = dict()
    try:
        validator.validate(attrs)
        result["valid"] = True
    except ValidationError as e:
        result["valid"] = False
        result["message"] = str(e)

    print(json.dumps(result))


if __name__ == "__main__":
    main()
