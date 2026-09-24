#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "parver",
# ]
# ///
"""Update version strings in structured files
(schemas, examples, version.py, changelog, tests).

Text files must be updated manually.
"""
import difflib
import functools
import json
import logging
import runpy
import subprocess as sp
import sys
from argparse import ArgumentParser
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from parver import Version

logger = logging.getLogger(__name__)
PROJECT_DIR = Path(__file__).resolve().parent.parent


def get_current_version() -> str:
    d = runpy.run_path(str(PROJECT_DIR / "_version.py"))
    return d["__version__"]


def sanitize_version(s: str) -> str:
    parsed = Version.parse(s)
    normalized = parsed.normalize()
    out = str(normalized)
    return out


@dataclass
class Args:
    new_version: str
    log_level: int
    execute: bool

    @classmethod
    def parse(cls, args=None):
        parser = ArgumentParser(description=__doc__)
        parser.add_argument("new_version", type=sanitize_version)
        parser.add_argument("-v", "--verbose", action="count", default=0)
        parser.add_argument(
            "--execute",
            action="store_true",
            help="write the changes; by default, just print the diff",
        )
        p = parser.parse_args(args)

        log_level = {
            0: logging.WARNING,
            1: logging.INFO,
            2: logging.DEBUG,
        }.get(p.verbose, logging.DEBUG)

        return cls(p.new_version, log_level, p.execute)


JSO = int | float | None | bool | str | list["JSO"] | dict[str, "JSO"]


class JsoUpdater:
    def __init__(
        self, old_version: str, new_version: str, key: str, substring=False
    ) -> None:
        self.old_version = old_version
        self.new_version = new_version
        self.key = key
        self.substring = substring

    def apply(self, jso: JSO) -> int:
        count = 0
        if jso is None or isinstance(jso, (int, float, bool, str)):
            return count
        elif isinstance(jso, list):
            for item in jso:
                count += self.apply(item)
        elif isinstance(jso, dict):
            val = jso.get(self.key)
            if isinstance(val, str):
                if self.substring:
                    if self.old_version in val:
                        jso[self.key] = val.replace(self.old_version, self.new_version)
                        count += 1
                elif self.old_version == val:
                    jso[self.key] = self.new_version
                    count += 1
            for v in jso.values():
                count += self.apply(v)
        else:
            raise TypeError(f"Unknown JSO type: {type(jso)}")

        return count


@dataclass
class Update:
    old: str
    new: str


class VersionUpdater:
    def __init__(self, old_version: str, new_version: str) -> None:
        self.old = old_version
        self.new = new_version
        self.mapping: dict[Path, Update] = {}

    def apply_updates(self) -> int:
        count = 0
        for path, update in self.mapping.items():
            path.write_text(update.new)
            count += 1
        return count

    def _update_example(self, fpath: Path) -> bool:
        """Handle examples which are JSONC files which might be a full zarr.json document,
        an attributes object, or an ome object, or something else.

        Currently does a dumb string replace.
        """
        orig = fpath.read_text()
        # if (ome := jso.get("attributes", {}).get("ome")) or (ome := jso.get("ome")):
        #     inner = ome
        # else:
        #     inner = jso

        # if inner.get("version") == self.old:
        #     inner["version"] = self.new
        #     self.mapping[fpath] = Update(orig, json.dumps(jso, indent=2) + "\n")
        #     return True
        old = f'"version": "{self.old}"'
        new = f'"version": "{self.new}"'
        if old in orig:
            updated = orig.replace(old, new)
            self.mapping[fpath] = Update(orig, updated)
            return True
        return False

    def _update_schema_id(self, jso: dict[str, JSO]) -> bool:
        s = jso.get("$id", "")
        if isinstance(s, str) and self.old in s:
            jso["$id"] = s.replace(self.old, self.new)
            return True
        else:
            return False

    def _update_version_schema(self) -> bool:
        p = PROJECT_DIR / "schemas" / "_version.schema"
        orig = p.read_text()
        jso = json.loads(orig)
        updated_id = self._update_schema_id(jso)
        if not updated_id:
            logger.warning("Did not update $id of %s", p)
        vals = []
        updated_enum = False

        for s in jso["enum"]:
            if s == self.old:
                vals.append(self.new)
                updated_enum = True
            else:
                vals.append(s)

        if not updated_enum:
            logger.warning("Did not update enum field of %s", p)

        if updated_enum or updated_id:
            self.mapping[p] = Update(orig, json.dumps(jso, indent=2))
            return True
        return False

    def _update_schema(self, fpath: Path) -> int:
        orig = fpath.read_text()
        jso = json.loads(orig)
        updated_id = self._update_schema_id(jso)
        updater = JsoUpdater(self.old, self.new, "$ref", True)
        count = updater.apply(jso)
        total = count + updated_id
        if total:
            self.mapping[fpath] = Update(orig, json.dumps(jso, indent=2) + "\n")
        return total

    def _update_schemas(self) -> int:
        count = 0
        for p in PROJECT_DIR.joinpath("schemas").glob("*.schema*"):
            if p.name.startswith("_") or not p.is_file():
                continue
            n_updates = self._update_schema(p)
            count += bool(n_updates)
        return count + self._update_version_schema()

    def _update_examples(self) -> int:
        count = 0
        for p in PROJECT_DIR.joinpath("examples").glob("**/*.json"):
            if p.name.startswith(".") or not p.is_file():
                continue
            count += self._update_example(p)
        return count

    def _update_version_py(self):
        fpath = PROJECT_DIR / "_version.py"
        orig = fpath.read_text()
        self.mapping[fpath] = Update(orig, f'__version__ = "{self.new}"\n')
        return True

    def _update_ome(self, ome: dict[str, JSO]) -> bool:
        if ome.get("version") == self.old:
            ome["version"] = self.new
            return True
        return False

    def _update_attributes(self, attributes: dict[str, JSO]) -> bool:
        ome = attributes.get("ome")
        if isinstance(ome, dict):
            return self._update_ome(ome)
        return False

    def _update_attributes_file(self, fpath: Path) -> bool:
        orig = fpath.read_text()
        jso = json.loads(orig)
        updated = self._update_attributes(jso)
        if updated:
            self.mapping[fpath] = Update(orig, json.dumps(jso, indent=2) + "\n")
            return True
        return False

    def _update_zarr_json_file(self, fpath: Path) -> bool:
        orig = fpath.read_text()
        jso = json.loads(orig)
        attrs = jso.get("attributes")
        if attrs is None:
            return False
        updated = self._update_attributes(attrs)
        if updated:
            self.mapping[fpath] = Update(orig, json.dumps(jso, indent=2) + "\n")
            return True
        return False

    def _update_zarr_hierarchy(self, dpath: Path) -> int:
        count = 0
        for fpath in dpath.glob("**/zarr.json"):
            count += self._update_zarr_json_file(fpath)
        return count

    def _update_zarr_tests(self) -> int:
        count = 0
        for dpath in PROJECT_DIR.joinpath("tests/zarr").glob("**/*.ome.zarr"):
            count += self._update_zarr_hierarchy(dpath)
        return count

    def _update_attributes_tests(self) -> int:
        count = 0
        for fpath in PROJECT_DIR.joinpath("tests/attributes").glob("**/*.json"):
            count += self._update_attributes_file(fpath)
        return count

    def _update_changelog(self):
        path = PROJECT_DIR.joinpath("version_history.md")
        orig = path.read_text()

        updated = orig.replace(
            "## Unreleased",
            f"## Unreleased\n\n## {self.new} - TBC",
        )
        if updated != orig:
            self.mapping[path] = Update(orig, updated)
            return True
        return False

    def plan_updates(self) -> int:
        count = 0
        count += self._update_examples()
        count += self._update_schemas()
        count += self._update_attributes_tests()
        count += self._update_zarr_tests()
        count += self._update_version_py()
        count += self._update_changelog()
        return count

    def list_updated_files(self) -> list[Path]:
        return sorted(self.mapping)

    def _format_diff(self, path: Path) -> str:
        update = self.mapping[path]
        fname = str(path.relative_to(PROJECT_DIR))
        n1 = f"{fname} v{self.old}"
        n2 = f"{fname} v{self.new}"
        return "\n".join(
            difflib.unified_diff(
                update.old.splitlines(),
                update.new.splitlines(),
                fromfile=n1,
                tofile=n2,
                lineterm="",
            )
        )

    def format_diffs(self, path: Path | None = None):
        if path is not None:
            yield self._format_diff(path)
            return

        for p in self.list_updated_files():
            yield self._format_diff(p)


def git_status():
    result = sp.run(
        ["git", "status", "--porcelain"], check=True, text=True, capture_output=True
    )
    s = result.stdout.strip()
    out = []
    if s:
        for line in s.splitlines():
            status = line[:2].strip()
            path = Path(line[3:])
            out.append((status, path))
    return out


@functools.wraps(print)
def eprint(*args, **kwargs):
    kwargs.setdefault("file", sys.stderr)
    print(*args, **kwargs)


def list_tracked_files() -> list[Path]:
    res = sp.run(
        ["git", "ls-tree", "-r", "HEAD", "--name-only"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [PROJECT_DIR / p for p in res.stdout.strip().splitlines(False)]


def find_remaining_old(old: str) -> list[Path]:
    ignore = {PROJECT_DIR / "uv.lock", PROJECT_DIR / "version_history.md"}
    return [
        p
        for p in sorted(list_tracked_files())
        if p not in ignore and old in p.read_text()
    ]


def format_list(items: Iterable, sep="\n", indent="\t"):
    return sep.join(f"{indent}{item}" for item in items)


def main(raw_args=None):
    args = Args.parse(raw_args)
    logging.basicConfig(level=args.log_level)
    old_version = get_current_version()

    updater = VersionUpdater(old_version, args.new_version)
    n_updates = updater.plan_updates()

    if not n_updates:
        logger.warning("No updates to make")
        return 0

    if args.execute:
        changes = git_status()
        if changes:
            print(
                f"You have {len(changes)} changed files in git. "
                "Commit or stash them before retrying with --execute.",
                file=sys.stderr,
            )
            return 1
        updater.apply_updates()
        eprint(f"Changed {n_updates} files.")
    else:
        sep = "\n\n" + ("-" * 80) + "\n\n"
        print(sep.join(updater.format_diffs()))
        eprint(f"Would change {n_updates} files. Use --execute to make changes.")

    remaining_old = find_remaining_old(old_version)

    if not args.execute:
        remaining_old = [x for x in remaining_old if x not in updater.mapping]

    if remaining_old:
        eprint(
            f"{len(remaining_old)} files may still have references to the old version:\n{format_list(remaining_old)}"
        )
        eprint(
            f"Find line references with\n\tgrep --color -n -F '{old_version}' $(git ls-tree -r HEAD --name-only)"
        )

    eprint(
        "N.B. version strings in free text like index.md must be updated manually",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
