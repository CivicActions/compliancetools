#!/usr/bin/env python

# Given a YAML file and path to directory of template files, this tool
# generates markdown files, replicating the directory structure in the template
# directory. It uses the https://github.com/CivicActions/secrender tool for
# variable replacement.

import os
import click
import secrender
from yaml import load, FullLoader
from yamlinclude import YamlIncludeConstructor

@click.command()
@click.option('--in', '-i', 'in_',
              required=True,
              type=click.Path(exists=True, dir_okay=False, readable=True),
              help='values (YAML)')
@click.option('--out', '-o', 'out_',
              type=click.Path(exists=True, dir_okay=True, readable=True),
              default='.',
              help='Output directory')
@click.option('--templates', '-t', 'template_dir',
              type=click.Path(exists=True, dir_okay=True, file_okay=False),
              help='Template directory')
def main(in_, template_dir, out_):
    template_args = load_template_args(in_)
    all_templates = get_template_list(template_dir)
    for template in all_templates:
        out_file = template.replace(template_dir, '')
        out_file = os.path.join(out_, out_file)
        ext = os.path.splitext(out_file)
        if ext[1] == '.j2':
            out_file = ext[0]
        if not os.path.exists(os.path.dirname(out_file)):
            os.makedirs(os.path.dirname(out_file))
        secrender.secrender(template, template_args, out_file)

def load_template_args(in_):
    YamlIncludeConstructor.add_to_loader_class(loader_class=FullLoader)
    with open(in_, "r") as stream:
        yaml = load(stream, Loader=FullLoader)
    return secrender.get_template_args(yaml, None, dict())

def get_template_list(template_dir):
    file_list = list()
    for (dirpath, dirname, filenames) in os.walk(template_dir):
        file_list += [os.path.join(dirpath, file) for file in filenames]
    return file_list

if __name__ == '__main__':
    main()