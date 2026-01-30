# %%
import os
import glob
from pathlib import Path
import jsonc as json
import logging

# Suppress warnings from json-schema-for-humans about unresolvable URLs
logging.getLogger().setLevel(logging.ERROR)

# change working directory to the location of this script
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def build_json_examples():
    """Build markdown files from json examples."""
    # glob recursively to find all json files
    input_directory = 'examples'
    output_directory = 'examples'
    os.makedirs(output_directory, exist_ok=True)

    # iterate over all folders in the examples directory
    example_types = [
        p for p in os.listdir(input_directory)
        if os.path.isdir(os.path.join(input_directory, p))
        ]

    index_md = """# NGFF metadata JSON Examples

This section contains JSON examples for various metadata layouts.
"""

    for root, subdirs, files in os.walk(input_directory):
        for subdir in subdirs:

            json_files = glob.glob(os.path.join(root, subdir, '*.json'), recursive=True)
            if not json_files:
                continue
            category = '_'.join(os.path.relpath(os.path.join(root, subdir), input_directory).split(os.sep))

            index_md += f"\n## {category}\n"

            # add header
            markdown_content = f"""# {category} Examples

This document contains JSON examples for {category} metadata layouts.

"""

            # append each json file content
            for json_file in json_files:
                print(f'Processing {json_file}...')

                crossref = f"examples:{category}:{Path(json_file).stem}"
                index_md += f"- [{Path(json_file).stem}](#{crossref})\n"

                json_file_name = Path(json_file).stem

                # Create the Markdown content
                markdown_content += f"""## {os.path.splitext(json_file_name)[0]}
({crossref})=

```{{literalinclude}} {Path(os.path.relpath(json_file, Path(json_file).parent)).as_posix()}
:linenos:
:language: json
```
"""
                with open(os.path.join(Path(json_file).parent, f'{category}.md'), 'w') as md_file:
                    md_file.write(markdown_content)

    with open(Path(output_directory) / "index.md", 'w') as index_file:
        index_file.write(index_md)

def build_json_schemas():
    from json_schema_for_humans.generate import generate_from_filename
    from json_schema_for_humans.generation_configuration import GenerationConfiguration
    import json

    schema_source_dir = 'schemas'
    output_directory = 'schemas'
    os.makedirs(output_directory, exist_ok=True)
    schema_files = glob.glob(os.path.join(schema_source_dir, '*.schema'), recursive=True)


    index_markdown = """# NGFF metadata JSON Schemas

This section contains JSON schemas for various metadata layouts.
Find below links to auto-generated markdown pages or interactive HTML pages for each schema.

| Schema | Markdown | HTML |
|--------|----------|------|
"""

    for schema_file in schema_files:
        if 'strict' in schema_file:
            continue  # skip strict schemas

        print(f'Processing {schema_file}...')
        output_path_md = os.path.join(output_directory, f"{Path(schema_file).stem}" + ".md")
        output_path_html = os.path.join(output_directory, f"{Path(schema_file).stem}" + ".html")
        os.makedirs(os.path.dirname(output_path_md), exist_ok=True)
        os.makedirs(os.path.dirname(output_path_html), exist_ok=True)        

        # Generate the documentation
        try:
            config_md = GenerationConfiguration(
                template_name='md',
                with_footer=True,
                show_toc=True,
                link_to_reused_ref=True,
                )
            generate_from_filename(
                os.path.abspath(schema_file),
                result_file_name=os.path.abspath(output_path_md),
                config=config_md
            )

            # insert mySt cross-reference at top of markdown files
            with open(output_path_md, 'r', encoding='utf-8') as md_file:
                md_content = md_file.read()
            crossref = f"schemas:{Path(schema_file).stem}"
            md_content = f"""---
author: ""
---
({crossref})=\n\n{md_content}
"""
            with open(output_path_md, 'w', encoding='utf-8') as md_file:
                md_file.write(md_content)

            link_markdown = f"[{Path(schema_file).stem}](#{crossref})"
        except Exception as e:
            print(f"Error generating markdown for {schema_file}: {e}")
            link_markdown = ""

        try:
            config_html = GenerationConfiguration(
                template_name='js',
                with_footer=True,
                show_toc=False,
                link_to_reused_ref=True,
                )

            generate_from_filename(
                os.path.abspath(schema_file),
                result_file_name=os.path.abspath(output_path_html),
                config=config_html
            )
            link_html = f"[{Path(schema_file).stem}]({output_path_html})"

        except Exception as e:
            print(f"Error generating HTML for {schema_file}: {e}")
            link_html = ""

        index_markdown += f"| {Path(schema_file).stem} | {link_markdown} | {link_html} |\n"

    with open(Path(output_directory) / "index.md", 'w') as index_file:
        index_file.write(index_markdown)

def build_footer():
    """Build footer file."""
    from datetime import datetime
    year = datetime.now().year
    footer_content = f"""
    <div>
        Copyright © 2020-{year}
        <a href="https://www.openmicroscopy.org/"><abbr title="Open Microscopy Environment">OME</abbr></a><sup>®</sup>.
        OME trademark rules apply.
    </div>
    """
    with open('footer.md', 'w') as footer_file:
        footer_file.write(footer_content)

def build_legacy_bikeshed(root: str = '.'):
    """Build legacy Bikeshed files."""
    import subprocess
    import glob
    import sys

    bikeshed_file = os.path.normpath(f"{root}/{glob.glob('*.bs')[0]}")
    subprocess.run([sys.executable, '-m', 'bikeshed', 'spec', bikeshed_file, 'index.html'], check=True)

build_json_examples()
build_json_schemas()
build_footer()
build_legacy_bikeshed()
