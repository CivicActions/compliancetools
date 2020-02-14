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
from pathlib import Path
from itertools import zip_longest, dropwhile

@click.command()
@click.option('--in', '-i', 'in_',
              required=True,
              type=click.Path(exists=True, dir_okay=False, readable=True),
              help='values (YAML)')
@click.option('--templates', '-t', 'template_dir',
              type=click.Path(exists=True, dir_okay=True, file_okay=False),
              help='Template directory')
@click.option('--out', '-o', 'out_',
              type=click.Path(exists=False, dir_okay=True, readable=True),
              default='.',
              help='Output directory')
def main(in_, template_dir, out_):
    template_args = load_template_args(in_)
    od = Path(out_)
    td = Path(template_dir)
    if not od.is_dir():
        od.mkdir(parents=True, exist_ok=True)

    p = Path(td).rglob("*")
    templates = [x for x in p if x.is_file()]

    for tf in templates:
        new_path = rewrite(tf, td, od)
        new_file = Path(new_path)
        ext = new_file.suffix
        if ext == '.j2':
            new_file = new_file.with_name(new_file.stem)

        if not new_file.parent.is_dir():
            new_file.parent.mkdir(parents=True, exist_ok=True)
        print("Creating file: {} from {}".format(new_file, tf))
        secrender.secrender(tf, template_args, new_file)

def load_template_args(in_):
    YamlIncludeConstructor.add_to_loader_class(loader_class=FullLoader)
    with open(in_, "r") as stream:
        yaml = load(stream, Loader=FullLoader)
    return secrender.get_template_args(yaml, None, dict())

def rewrite(tf, td, od):
    subpath = [p[0] for p in dropwhile(lambda f: f[0] == f[1], zip_longest(tf.parts, td.parts))]
    return str(od / Path(*subpath))

if __name__ == '__main__':
    main()