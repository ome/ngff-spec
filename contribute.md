---
author: ""
---
# Contribution guide

Contributions to the spec text, examples and schemas are highly welcome
and appreciated by the ngff community.
If you propose an RFC (i.e., major change) or a a minor change (pull request),
please make sure to follow [these guidelines](https://ngff.openmicroscopy.org/contributing/index.html).

Major changes should follow the RFC process as it was laid out in [RFC1](https://ngff.openmicroscopy.org/rfc/1/index.html).

## Building the documentation

Build and inspect changes to the documentation before submitting a PR.
To do so, you first need to install the necessary dependencies:

```bash
pip install .
```

This document uses [jupyter-book](https://jupyterbook.org) to generate the pages
and [MyST](https://mystmd.org) markdown for formatting.
After installing these via the dependencies,
navigate into the repository on your machine and build the book using the following command:

```bash
python pre_build.py
jupyter book start
```

This will build the book and start a local server to inspect the changes in your browser.

## First contribution

If you haven't contributed to the spec before,
please add yourself as an author in the `myst.yml` metadata file.
This should look like this, for example:

```yaml
    - name: John A. Doe
      id: jdoe
      orcid: xxxx-xxxx-xxxx-xxxx
      github: jdoe
      affiliations:
        - id: key
          institution: ICSLDJ University
          city: Doeburg
          ror: https://ror.org/....
    - name: Jane Doe
      affiliations: key
```

For more information see [myst documentation on author formatting](https://mystmd.org/guide/frontmatter#frontmatter-authors).

When you submit your first PR,
make sure to rebuild the `CITATION.cff` file in the root of this repository.
To do so, run the following command:

```bash
jupyter book build --cff
```

Make sure the updated `CITATION.cff` file is included in your PR.

### Text format

Contributions should conform to [Semantic Line Breaks (SemBr)](https://sembr.org/),
to improve change tracking.

### Formatting hints

The specification uses MyST extensively for a number of formatting options
to make the text readable and improve structure.

#### Referencing

MyST allows a number of ways to reference and cross-reference inside this text
and across several of the pages in this repo.
For an overview of supported referencing syntax,
see the [MyST doc pages](https://mystmd.org/guide/cross-references).
It is recommended to use the following syntax in this document for consistency:

```
anchor: (your-reference-name)=
reference: [This is a reference](#your-reference-name)
```

#### Admonitions

We suggest using [admonitions](https://mystmd.org/guide/admonitions) for example code and other highlighting.
For examples, please use the following syntax to highlight your examples:

`````markdown
````{admonition} Example

Some informative text about your example
```json
"key": "value"
```
````
`````

which results in

````{admonition} Example

Some informative text about your example
```json
"key": "value"
```
````

If you want to link in example metadata from somewhere in this repo (i.e, a json file),
use this syntax:

`````markdown
````{admonition} Example

Some informative text about your example
```{literalinclude} path/to/example.json
:language: json
:linenos:
:tab-width: 2
```
````
`````

Other useful admonitions (e.g., `hint`, `note`) can be found [here](https://mystmd.org/guide/directives).
