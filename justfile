_:
    just --list

# Build the specification in the _build/ directory.
build:
    uv run python pre_build.py
    uv run jupyter book build --html --ci

# Check spelling in the source files;
# configured in pyproject.toml.
spell:
    uv run --extra testing codespell

# Run all lint commands.
lint: spell

# Run schema tests.
test:
    uv run --extra testing pytest -v
