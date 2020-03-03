#!/usr/bin/env python

# Copyright 2019-2020 CivicActions, Inc. See the README file at the top-level
# directory of this distribution and at https://github.com/CivicActions/compliancetools#copyright.

import click
import yaml
from pathlib import Path
import csv

@click.command()
@click.option("--in", "-i", "in_",
              required=False,
              default="components",
              type=click.Path(exists=True, file_okay=False, dir_okay=True),
              help="The path to the components directory.")
@click.option("--cert", "-c", "cert",
              required=False,
              default="fisma-low-impact",
              type=click.Choice([
                  'dhs-4300a',
                  'fedramp-high',
                  'fedramp-low',
                  'fedramp-moderate',
                  'fedramp-tailored'
                  'fisma-high-impact',
                  'fisma-low-impact',
                  'fisma-mod-impact',
                  'icd-503-high',
                  'icd-503-low',
                  'icd-503-moderate',
                ], case_sensitive=True),
              help="The certification to use to create the matrix.")
def main(in_, cert):
    header, controls = getComponents(in_)
    createMatrix(header, controls, cert)

def getComponents(components_dir):
    p = Path(components_dir).rglob("*.yaml")
    filelist = [x for x in p if x.is_file()]
    controls = {}
    header = {"id": "Control ID", "name": "Name"}
    for f in filelist:
        if f.name != "component.yaml":
            entity = f.parent.name
            header.update({entity: entity})
            with open(f, "r") as stream:
                try:
                    control = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
            for s in control["satisfies"]:
                key = s["control_key"]

                if "implementation_status" in s:
                    status = s["implementation_status"]
                else:
                    status = ""

                if key not in controls:
                    controls.update({key: {"name": s["control_name"], "id": key}})
                controls[key].update({entity: status})

    return header, controls

def createMatrix(header, controls, cert):
    c = Path('/var/lib/certifications/' + cert + '.yaml')
    f = Path(c)
    try:
        f_absolute = f.resolve(strict=True)
    except FileNotFoundError as e:
        print(e)

    print('Creating responsibility matrix based on certification: {}'.format(cert))
    with open(f, "r") as stream:
        try:
            opencontrol = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

        rows = []
        header_row = []
        for k, h in header.items():
            header_row.append(h)
        rows.append(header_row)
        header.pop("id", None)
        for c in opencontrol["standards"]["NIST-800-53"]:
            row = []
            row.append(c)
            for i, v in header.items():
                if c in controls and i in controls[c]:
                    row.append(controls[c][i])
                else:
                    row.append("")
            rows.append(row)
    print('Creating file responsibility_matrix.csv')
    with open("responsibility_matrix.csv", "w+") as stream:
        writer = csv.writer(stream)
        writer.writerows(rows)

if __name__ == "__main__":
    main()