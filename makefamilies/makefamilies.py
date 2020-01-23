#!/usr/bin/env python

from os import path, walk, mkdir, system
import ssp, opencontrol
import rtyaml
import datetime

def main():
    parent = path.abspath(path.join(path.dirname( __file__ )))
    controls_dir = path.join(parent,'docs/controls')
    oc_yaml = path.join(parent, 'opencontrol.yaml')
    project = opencontrol.load_project_from_path(parent)
    project_yaml = opencontrol.load_opencontrol_yaml(oc_yaml, "system", ("1.0.0",))
    compiled_date = datetime.datetime.today()
    families = []
    # Create a list of all of the components in the project.s
    for component in project_yaml['components']:
        for (dirpath, dirnames, filenames) in walk(component):
            families.extend(filenames)
            break
        families.sort()

    if not path.exists(controls_dir):
        mkdir(controls_dir)

    # Create component files.
    for family in list(dict.fromkeys(families)):
        fam_abbr = family[:2]
        if fam_abbr.isupper():
            control_file = path.join(controls_dir, fam_abbr+'.md')
            with open(control_file, 'w') as output:
                print(ssp.build_ssp(project, {
                    "include-control-descriptions": True,
                    "only-family": fam_abbr,
                }), file=output)
                output.close()

    # Create Table of Contents file.
    print("Creating controls.md index.")
    with open(path.join(parent, 'docs/controls.md'), 'w') as comp:
        print("# Controls (compiled: {})\n".format(compiled_date.strftime("%Y.%m.%d at %H%M")),
        file=comp)
        comp.close()

    system(r"cd docs && gh-md-toc controls/* | sed '/^           /d' | sed '/^   \*/d' | sed 's/^      //' | sed 's/^\(Created by \[gh-md-toc\].*$\)/<!-- \1 -->/'>> controls.md")

if __name__ == '__main__':
    main()
