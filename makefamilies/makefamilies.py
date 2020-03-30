#!/usr/bin/env python

# Copyright 2019-2020 CivicActions, Inc. See the README file at the top-level
# directory of this distribution and at https://github.com/CivicActions/compliancetools#copyright.

import rtyaml
import datetime
import click
from grc import ssp
from grc import opencontrol
from pathlib import Path

@click.command()
@click.option('--out', '-o', 'out_',
              type=click.Path(exists=False, dir_okay=True, readable=True),
              default='docs/controls',
              help='Output directory')
def main(out_):
    base = Path()
    controls_dir = base.joinpath(out_)
    if not controls_dir.exists():
        print("Creating output directory {}".format(controls_dir.resolve(strict=False)))
        controls_dir.mkdir(exist_ok=False)

    oc_yaml = base.joinpath('opencontrol.yaml')

    try:
        oc_yaml_abs = oc_yaml.resolve(strict=True)
    except FileNotFoundError:
        print("No opencontrol.yaml file!")

    project = opencontrol.load_project_from_path(base)
    project_yaml = opencontrol.load_opencontrol_yaml(oc_yaml_abs, "system", ("1.0.0",))
    families = []
    # Create a list of all of the components in the project.s
    for component in project_yaml['components']:
        p = Path(component).rglob("*")
        files = [x.name for x in p if x.is_file()]
        families.extend(files)
        families.sort()

    # Create component files.
    for family in list(dict.fromkeys(families)):
        fam_abbr = family[:2]
        if fam_abbr.isupper():
            control_file = controls_dir.joinpath(fam_abbr+'.md')
            with open(control_file, 'w') as output:
                print("Creating {}".format(control_file))
                print(ssp.build_ssp(project, {
                    "include-control-descriptions": True,
                    "only-family": fam_abbr,
                }), file=output)
                output.close()

if __name__ == '__main__':
    main()
