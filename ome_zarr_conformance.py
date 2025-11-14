#!/usr/bin/env python3
"""
Test with

```sh
./ome_zarr_conformance.py zarr -- sh -c 'echo "{\"valid\": true}"'
```
"""

from __future__ import annotations
from concurrent.futures import Future, ThreadPoolExecutor
import os
import subprocess as sp
from argparse import ArgumentParser
from pathlib import Path
import sys
import re
import json
from dataclasses import dataclass
from typing import Any, Iterable, Literal, Self
import logging

logger = logging.getLogger("ome_zarr_conformance")

here = Path(__file__).resolve().parent
tests_dir = here / "tests"


@dataclass
class CommandOutput:
    valid: bool
    message: str | None

    @classmethod
    def from_jso(cls, jso: dict[str, Any]) -> Self:
        return cls(jso["valid"], jso.get("message"))


@dataclass
class TestResult:
    test_name: str
    status: Literal["pass", "fail", "error"]
    message: str | None
    stderr: str
    return_code: int
    conformance: Conformance | None = None


@dataclass
class Conformance:
    strict: bool
    valid: bool
    description: bool | None

    @classmethod
    def from_jso(cls, jso: dict[str, Any]) -> Self:
        return cls(
            strict=jso.get("strict", False),
            valid=jso.get("valid", True),
            description=jso.get("description"),
        )

    @classmethod
    def from_attributes(cls, attrs: dict[str, Any], pop=False) -> Self:
        if pop:
            conformance_jso = attrs.pop("_conformance", {})
        else:
            conformance_jso = attrs.get("_conformance", {})
        return cls.from_jso(conformance_jso)

    @classmethod
    def from_attributes_file(cls, fpath: Path) -> Self:
        content = fpath.read_text()
        jso: dict[str, Any] = json.loads(content)
        return cls.from_attributes(jso)


class Requested:
    def __init__(
        self,
        exclude_patterns: list[re.Pattern] | None = None,
        include_patterns: list[re.Pattern] | None = None,
        exclude_strict=False,
        exclude_invalid=False,
    ) -> None:
        self.exclude_patterns = exclude_patterns or []
        self.include_patterns = include_patterns or []

        if exclude_strict:
            self.exclude_patterns.append(re.compile(r"^strict/"))
        if exclude_invalid:
            self.exclude_patterns.append(re.compile(r"(^|strict/)invalid/"))

    def include(self, name: str) -> bool:
        if self.exclude_patterns and any(p.search(name) for p in self.exclude_patterns):
            return False
        if self.include_patterns and not any(
            p.search(name) for p in self.include_patterns
        ):
            return False
        return True


def test_path_to_name(fpath: Path, root: Path) -> str:
    w_suff = str(fpath.relative_to(root)).replace(os.path.sep, "/")
    return w_suff.split(".", 1)[0]


def run_test(dingus_cmd: list[str], fpath: Path, test_name: str) -> TestResult:
    test_logger = logger.getChild(test_name)

    components = test_name.split("/")
    is_strict = components[0] == "strict"
    valid_idx = 1 if is_strict else 0
    if components[valid_idx] == "invalid":
        is_valid = False
    elif components[valid_idx] == "valid":
        is_valid = True
    else:
        raise RuntimeError(f"cannot determine validity from name: {test_name}")

    res = sp.run(
        dingus_cmd + [os.fspath(fpath)],
        text=True,
        capture_output=True,
    )

    if res.returncode:
        test_logger.error(
            "error (exit code %s):%s",
            res.returncode,
            "\n" + res.stderr if res.stderr else "",
        )
        return TestResult(test_name, "error", None, res.stderr, res.returncode)

    out: CommandOutput = CommandOutput.from_jso(json.loads(res.stdout))
    if out.valid == is_valid:
        test_logger.debug("pass: %s", out.message or "")
        return TestResult(test_name, "pass", out.message, res.stderr, res.returncode)
    else:
        test_logger.warning(
            "fail (expected %svalid): %s%s",
            "" if is_valid else "in",
            out.message or "",
            "\n" + res.stderr if res.stderr else "",
        )
        return TestResult(test_name, "fail", out.message, res.stderr, res.returncode)


def run_all_tests(
    cmd: list[str],
    cases: dict[str, Path],
    threads=None,
) -> Iterable[TestResult]:
    with ThreadPoolExecutor(threads) as pool:
        logger.info(
            "Running %s tests with max %s threads", len(cases), pool._max_workers
        )
        futs: list[Future] = []
        for name, path in cases.items():
            futs.append(pool.submit(run_test, cmd, path, name))

        for f in futs:
            res = f.result()
            if res is not None:
                yield res


def main(raw_args=None):
    parser = ArgumentParser(
        description=(
            "Feed sample Zarr data into a dingus CLI for validation. "
            "After the arguments shown, add a -- followed by the dingus CLI call; "
            "e.g., `ome_zarr_conformance attributes --exclude-strict -- path/to/my/dingus -cli +args`. "
            "The path to the attributes file or root of the zarr container will be appended to the dingus call."
        )
    )
    parser.add_argument(
        "mode",
        choices=["attributes", "zarr"],
        help=("whether to test single attributes documents or full zarr hierarchies."),
    )
    parser.add_argument(
        "--no-exit-code",
        "-X",
        action="store_true",
        help="return exit code 0 (success) even if tests failed",
    )
    parser.add_argument(
        "--include-pattern",
        "-p",
        type=re.compile,
        action="append",
        help="regular expression pattern for tests to include; can be given multiple times",
    )
    parser.add_argument(
        "--exclude-pattern",
        "-P",
        type=re.compile,
        action="append",
        help="regular expression pattern for tests to exclude; can be given multiple times",
    )
    parser.add_argument(
        "--exclude-strict",
        "-S",
        action="store_true",
        help="exclude strict tests",
    )
    parser.add_argument(
        "--exclude-invalid",
        "-I",
        action="store_true",
        help="exclude tests for invalid attributes",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        help="increase logging verbosity; can be repeated",
    )

    if raw_args is None:
        raw_args = sys.argv

    try:
        split = raw_args.index("--")
        dingus_args = raw_args[split + 1 :]
        these_args = raw_args[1:split]
    except ValueError:
        these_args = raw_args
        dingus_args = None

    args = parser.parse_args(these_args)

    lvl = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG,
    }.get(args.verbose, logging.DEBUG)
    logging.basicConfig(level=lvl)
    logging.debug("Got args: %s", args)

    if dingus_args is None:
        print(
            "No dingus command provided; add -- followed by the command",
            file=sys.stderr,
        )
        sys.exit(0)

    passes = 0
    failures = 0
    errors = 0

    match args.mode:
        case "attributes":
            dpath = tests_dir / "attributes"
            rglob = "*.json"
        case "zarr":
            dpath = tests_dir / "zarr"
            rglob = "*.ome.zarr"
        case _:
            raise RuntimeError("unreachable")

    req = Requested(
        exclude_patterns=args.exclude_pattern,
        include_patterns=args.include_pattern,
        exclude_strict=bool(args.exclude_strict),
        exclude_invalid=bool(args.exclude_invalid),
    )

    test_paths = ((test_path_to_name(p, dpath), p) for p in dpath.rglob(rglob))
    cases = dict(sorted((n, p) for n, p in test_paths if req.include(n)))

    for res in run_all_tests(
        dingus_args,
        cases,
    ):
        row = [
            res.test_name,
            res.status,
        ]
        if res.status == "pass":
            passes += 1
        elif res.status == "fail":
            failures += 1
        elif res.status == "error":
            errors += 1

        print("\t".join(row))

    logger.info("Got %s passes, %s failures, %s errors", passes, failures, errors)

    if args.no_exit_code:
        sys.exit(0)

    code = 0
    if failures:
        code += 1
    if errors:
        code += 2
    sys.exit(code)


if __name__ == "__main__":
    main()
