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
    uv run codespell

# Rebuild the `CITATION.cff` file from `myst.yml`.
cff:
    uv run jupyter book build --cff

# Run all lint commands.
lint: spell pre-commit

# Run schema tests.
test:
    uv run pytest -v

# Install pre-commit hooks to lint changed files.
pre-commit-install:
    uv run prek install

# Run pre-commit lints on all files.
pre-commit:
    uv run prek run --all-files

clean:
    rm -rf \
        _build \
        footer.md \
        _authors.md \
        examples/*.md \
        examples/**/*.md \
        schemas/*.md \
        schemas/**/*.md \
        schemas/**/*.html \
        schemas/**/*.css \
        schemas/**/*.js
