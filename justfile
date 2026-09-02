_:
    just --list

_prebuild:
    uv run python pre_build.py

# Build the specification in the _build/ directory.
build: _prebuild
    uv run jupyter book build --html --ci

# Build the book and start a local server to view it.
serve: _prebuild
    uv run jupyter book start

# Check spelling in the source files;
# configured in pyproject.toml.
spell:
    uv run --extra testing codespell

# Rebuild the `CITATION.cff` file from `myst.yml`.
cff:
    uv run jupyter book build --cff

# Run all lint commands.
lint: spell

# Run schema tests.
test:
    uv run --extra testing pytest -v
