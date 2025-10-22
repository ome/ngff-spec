# %%
import os
import glob
from pathlib import Path
import jsonc as json

# change working directory to the location of this script
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def build_json_examples():
    """Build markdown files from json examples."""
    # glob recursively to find all json files
    input_directory = 'examples'
    output_directory = '_generated/examples'
    os.makedirs(output_directory, exist_ok=True)
    example_types = os.listdir(input_directory)

    index_md = """---
title: NGFF metadata JSON Examples
short_title: JSON Examples
---

This section contains JSON examples for various metadata layouts.
"""

    for example in example_types:
        json_files = glob.glob(os.path.join(input_directory, example, '*.json'), recursive=True)
        markdown_file_name = os.path.join(output_directory, f'{example}.md')

        index_md += f"\n## {example}\n"

        # add header
        markdown_content = f"""# {example}\n\n

This document contains JSON examples for {example} metadata layouts.

"""


        # append each json file content
        for json_file in json_files:
            print(f'Processing {json_file}...')

            crossref = f"examples:{example}:{Path(json_file).stem}"
            index_md += f"- [{Path(json_file).stem}](#{crossref})\n"

            json_file_name = Path(json_file).stem

            # Create the Markdown content
            markdown_content += f"""
## {os.path.splitext(json_file_name)[0]}
({crossref})=

```{{literalinclude}} {os.path.abspath(json_file)}
:linenos:
:tab-width: 2
:language: json

```
"""
        # create 
        with open(markdown_file_name, 'w') as md_file:
            md_file.write(markdown_content)

    with open(os.path.join("examples.md"), 'w') as index_file:
        index_file.write(index_md)

def build_json_schemas():
    from json_schema_for_humans.generate import generate_from_filename
    from json_schema_for_humans.generation_configuration import GenerationConfiguration

    schema_source_dir = 'schemas'
    output_directory = '_generated/schemas'
    os.makedirs(output_directory, exist_ok=True)
    schema_files = glob.glob(os.path.join(schema_source_dir, '*.schema'), recursive=True)

    index_markdown = """# JSON Schemas

This section contains JSON schemas for various metadata layouts.
Find below links to auto-generated markdown pages or interactive HTML pages for each schema.

| Schema | Markdown | HTML |
|--------|----------|------|
"""

    for schema_file in schema_files:
        if 'strict' in schema_file:
            continue  # skip strict schemas

        print(f'Processing {schema_file}...')
        output_path_md = os.path.join(output_directory, "markdown", f"{Path(schema_file).stem}" + ".md")
        output_path_html = os.path.join(output_directory, "html", f"{Path(schema_file).stem}" + ".html")
        os.makedirs(os.path.dirname(output_path_md), exist_ok=True)
        os.makedirs(os.path.dirname(output_path_html), exist_ok=True)        

        # Generate the documentation
        try:
            config_md = GenerationConfiguration(
                template_name='md',
                with_footer=True,
                show_toc=False,
                link_to_reused_ref=False)
            generate_from_filename(
                os.path.abspath(schema_file),
                result_file_name=os.path.abspath(output_path_md),
                config=config_md
            )

            # insert mySt cross-reference at top of markdown files
            with open(output_path_md, 'r') as md_file:
                md_content = md_file.read()
            crossref = f"schemas:{Path(schema_file).stem}"
            md_content = f"({crossref})=\n\n{md_content}"
            with open(output_path_md, 'w') as md_file:
                md_file.write(md_content)

            link_markdown = f"[{Path(schema_file).stem}](#{crossref})"
        except Exception:
            link_markdown = ""

        try:
            config_html = GenerationConfiguration(
                template_name='js',
                with_footer=True,
                show_toc=False,
                link_to_reused_ref=False)

            generate_from_filename(
                os.path.abspath(schema_file),
                result_file_name=os.path.abspath(output_path_html),
                config=config_html
            )
            link_html = f"[{Path(schema_file).stem}]({output_path_html})"

        except Exception:
            link_html = ""

        index_markdown += f"| {Path(schema_file).stem} | {link_markdown} | {link_html} |\n"

    with open(os.path.join("schemas.md"), 'w') as index_file:
        index_file.write(index_markdown)

def build_footer():
    """Build footer file."""
    from datetime import datetime
    year = datetime.now().year
    footer_content = f"""
<div>
    Copyright © 2020-{year}
    <a href="https://www.openmicroscopy.org/"><abbr title="Open Microscopy Environment">OME</abbr></a><sup>®</sup>
    (<a href="https://dundee.ac.uk/"><abbr title="University of Dundee">U. Dundee</abbr></a>).
    OME trademark rules apply.
</div>
"""
    with open('footer.md', 'w') as footer_file:
        footer_file.write(footer_content)

build_json_examples()
build_json_schemas()
build_footer()
