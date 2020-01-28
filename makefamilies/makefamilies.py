#!/usr/bin/env python

import os
from grc import ssp
from grc import opencontrol
import rtyaml
import datetime
from pathlib import Path

def main():
    parent = Path()
    controls_dir = parent.joinpath('docs/controls')
    if not controls_dir.exists():
      os.makedirs(controls_dir)

    oc_yaml = parent.joinpath('opencontrol.yaml')

    try:
        oc_yaml_abs = oc_yaml.resolve(strict=True)
    except FileNotFoundError:
        print("No opencontrol.yaml file!")

    project = opencontrol.load_project_from_path(parent)
    project_yaml = opencontrol.load_opencontrol_yaml(oc_yaml, "system", ("1.0.0",))
    compiled_date = datetime.datetime.today()
    families = []
    # Create a list of all of the components in the project.s
    for component in project_yaml['components']:
        for (dirpath, dirnames, filenames) in os.walk(component):
            families.extend(filenames)
            break
        families.sort()

    # Create component files.
    for family in list(dict.fromkeys(families)):
        fam_abbr = family[:2]
        if fam_abbr.isupper():
            control_file = controls_dir.joinpath(fam_abbr+'.md')
            with open(control_file, 'w') as output:
                print(ssp.build_ssp(project, {
                    "include-control-descriptions": True,
                    "only-family": fam_abbr,
                }), file=output)
                output.close()

    # Create Table of Contents file.
    print("Creating controls.md index.")
    with open(parent.joinpath('docs/controls.md'), 'w') as comp:
        print("# Controls (compiled: {})\n".format(compiled_date.strftime("%Y.%m.%d at %H%M")),
        file=comp)
        comp.close()

    os.system(r"cd docs && gh-md-toc controls/* | sed '/^           /d' | sed '/^   \*/d' | sed 's/^      //' | sed 's/^\(Created by \[gh-md-toc\].*$\)/<!-- \1 -->/'>> controls.md")

if __name__ == '__main__':
    main()
