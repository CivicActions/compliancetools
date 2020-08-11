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
              help="The path to the components directory (default: ./components)")
@click.option("--cert", "-c", "cert",
              required=False,
              default="fisma-low-impact",
              type=click.Path(exists=False, dir_okay=True, readable=True),
              help="The certification to use to create the matrix (default: fisma-low-impact)")
@click.option("--privacy", "-p", "privacy",
              required=False,
              default=0,
              help="Include the Rev 4 Privacy controls in the matrix.")

def main(in_, cert, privacy):
    header, controls = getComponents(in_, privacy)
    createMatrix(header, controls, cert, privacy)

def getComponents(components_dir, privacy):
    p = Path(components_dir).rglob("*.yaml")
    filelist = [x for x in p if x.is_file()]
    controls = {}
    header = {"id": "Control ID", "name": "Name", "status": "Status"}
    with open('keys/status.yaml', "r", newline="") as st:
        statuses = yaml.safe_load(st)
    for f in filelist:
        if f.name != "component.yaml":
            entity = f.parent.name
            header.update({entity: entity})
            with open(f, "r", newline="") as stream:
                try:
                    control = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
            for s in control["satisfies"]:
                key = s["control_key"]
                if "implementation_status" in s:
                    implements = "x"
                else:
                    implements = ""

                if key not in controls:
                    controls.update({key: {"name": s["control_name"], "id": key}})
                controls[key].update({entity: implements})

                status_key = key.replace('_(', '(').replace('-0', '-')
                if status_key in statuses:
                    controls[key].update({"status": statuses[status_key]["implementation_status"]})

    return header, controls

def appendPrivacy(controls):
    p = Path().cwd().joinpath('certifications/privacy.yaml')
    with open(p, "r", newline="") as pr:
        priv = yaml.safe_load(pr)
    return {**controls["standards"]["NIST-800-53"], **priv["standards"]["NIST-800-53"]}

def createMatrix(header, controls, cert, privacy):
    f = Path('/var/lib/certifications/' + cert + '.yaml')

    try:
        f.resolve(strict=True)
    except FileNotFoundError as e:
        print(e)

    print('Creating responsibility matrix based on certification: {}'.format(cert))
    with open(f, "r", newline="") as stream:
        try:
            opencontrol = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

        if privacy:
            ctrl = appendPrivacy(opencontrol)
        else:
            ctrl = opencontrol["standards"]["NIST-800-53"]

        rows = []
        header_row = []
        for k, h in header.items():
            header_row.append(h)
        rows.append(header_row)
        header.pop("id", None)
        for c in ctrl:
            row = []
            row.append(c)
            for i, v in header.items():
                if c in controls and i in controls[c]:
                    row.append(controls[c][i])
                else:
                    row.append("")
            rows.append(row)
    print('Creating file responsibility_matrix.csv')
    with open("responsibility_matrix.csv", "w+", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerows(rows)

if __name__ == "__main__":
    main()
