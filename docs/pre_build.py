# %%
import os
import json
import glob
from pathlib import Path
import jsonc as json
import yaml

# %%
# change working directory to the location of this script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# %%
# glob recursively to find all json files
input_directory = '../examples'
output_directory = 'examples'
os.makedirs(output_directory, exist_ok=True)
example_types = os.listdir(input_directory)


md_files = []

for example in example_types:
    json_files = glob.glob(os.path.join(input_directory, example, '*.json'), recursive=True)

    example_directory = os.path.join(output_directory, example)    
    markdown_file_name = os.path.join(output_directory, f'{example}.md')

    # add header
    markdown_content = f"""# {example}\n\n

This document contains JSON examples for {example} metadata layouts.

"""

    # append each json file content
    for json_file in json_files:
        print(f'Processing {json_file}...')
        with open(json_file, 'r') as file:
            json_data = json.load(file)
        json_str = json.dumps(json_data, indent=4)
        json_file_name = Path(json_file).stem

        # Create the Markdown content
        markdown_content += f"""
## {os.path.splitext(json_file_name)[0]}
(examples:{example}:{Path(json_file).stem})=

```{{code-block}} json
:caption: {json_file_name}
:linenos:

{json_str}
```
"""

    # create 
    with open(markdown_file_name, 'w') as md_file:

        md_file.write(markdown_content)
    md_files.append(markdown_file_name)

# %% [markdown]
# ## json schema

# %%
from json_schema_for_humans.generate import generate_from_filename
from json_schema_for_humans.generation_configuration import GenerationConfiguration

schema_source_dir = '../schemas'
output_directory = 'schemas'
schema_files = glob.glob(os.path.join(schema_source_dir, '*.schema'), recursive=True)

for schema_file in schema_files:
    output_md_path = os.path.join(output_directory, f"{Path(schema_file).stem}.md")
    print(f'Processing {schema_file}...')

    # Generate the documentation
    config = GenerationConfiguration(
        template_name='md',
        with_footer=True,
        show_toc=True,
        link_to_reused_ref=False)
    try:
        generate_from_filename(
            schema_file,
            result_file_name=output_md_path,
            config=config
        )
    except Exception as e:
        print(f"Error processing {schema_file}: {e}")
