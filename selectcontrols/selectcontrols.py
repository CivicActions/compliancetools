#!/usr/bin/env python

import click
import copy
from itertools import zip_longest, dropwhile
from pathlib import Path
import rtyaml
import shutil

class Logger:
    
    def __init__(self, verbose):
        self.verbose = verbose
        
    def print(self, *args):
        if self.verbose:
            print(*args)

@click.command()
@click.option('--selection', '-s',
              type=click.File(),
              help='selected controls (YAML)')
@click.option('--in', '-i', 'template_dir',
              type=click.Path(exists=True, dir_okay=True, file_okay=False),
              required=True,
              help='Input directory tree')
@click.option('--out', '-o', 'out_',
              type=click.Path(exists=False, dir_okay=True, readable=True),
              default='.',
              help='Output directory')
@click.option('--verbose', '-V', is_flag=True)
def main(selection, template_dir, out_, verbose):
    template_path = Path(template_dir)
    output_path = Path(out_)
    selection = load_selection(selection)
    logger = Logger(verbose)
    
    if not output_path.is_dir():
        logger.print("Creating output directory {}".format(output_path))
        output_path.mkdir(parents=True, exist_ok=True)

    for template_file in Path(template_path).rglob("*"):
        if template_file.is_file():
            process(selection, template_file, template_path, output_path, logger)

def load_selection(selection):
    if selection:
        objects = rtyaml.load(selection)
        standards = objects['standards']
        return set((standard, control_key) for standard in standards for control_key in standards[standard])
    else:
        return None

def process(selection, template_file, template_path, output_path, logger):
    logger.print("Checking {}".format(template_file))
    try:
        with open(template_file) as fp:
            output_file = rewrite(template_file, template_path, output_path)
            output_file_p = Path(output_file)
            if not output_file_p.parent.is_dir():
                output_file_p.parent.mkdir(parents=True, exist_ok=True)

            if template_file.name == 'component.yaml':
                logger.print("  Copying {} to {}".format(template_file, output_file))
                shutil.copy(template_file, output_file)
            else:
                object = rtyaml.load(fp)
                object = select_controls(object, selection)
                controls = sorted(control['control_key'] for control in object['satisfies'])
                logger.print("  Writing controls to {}".format(output_file))
                for control in controls:
                    logger.print("    {}".format(control))
                with open(output_file, "w") as out:
                    rtyaml.dump(object, out)
                    
    except Exception as e:
        print("Exception {} processing {}".format(e, template_file))

def is_selected(control, selection):
    if selection is None:
        return True

    key = (control['standard_key'], control['control_key'])
    return key in selection

def select_controls(object, selection):
    edited = copy.deepcopy(object)
    edited['satisfies'] = [control for control in edited['satisfies']
                           if is_selected(control, selection)]
    return edited

def rewrite(tf, td, od):
    subpath = [p[0] for p in dropwhile(lambda f: f[0] == f[1], zip_longest(tf.parts, td.parts))]
    return str(od / Path(*subpath))

if __name__ == '__main__':
    main()
    
