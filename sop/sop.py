#!/usr/bin/env python

import re
from pathlib import Path

import click
import yaml  # type: ignore
from sop_writer import SopWriter

# Copyright 2019-2020 CivicActions, Inc. See the README file at the top-level
# directory of this distribution and at https://github.com/CivicActions/compliancetools#copyright.


def aggregate_control_data(component_dir: Path) -> dict:
    """
    Collect all the rendered Components YAML files and aggregate them by family.

    :param component_dir: a pathlib object file path object.
    :return: a dictionary with all the Controls sorted by Family.
    """

    families: dict = {}
    components = component_dir.rglob("*")
    templates = [
        cfile
        for cfile in components
        if cfile.is_file() and cfile.name != "component.yaml"
    ]
    for template in templates:
        family = template.stem.lower().replace("_", "-")
        if family not in families:
            families[family] = {}

        with open(template, "r") as tmpy:
            component = yaml.load(tmpy, Loader=yaml.FullLoader)
        satisfies = component.get("satisfies")
        for control in satisfies:
            control_id = control.get("control_key")
            if "(" in control_id:
                control_key = create_sortable_id(control_id.strip().lower(), "extended")
            else:
                control_key = create_sortable_id(control_id.strip().lower(), "simple")
            control_name = control.get("control_name").title()
            key = f"{control_key} {control_name}"
            if key and key not in families[family]:
                families[family][key] = {}

            for parts in control.get("narrative"):
                part = parts.get("key", "text")

                if part not in families[family][key]:
                    families[family][key][part] = []
                families[family][key][part].append(parts.get("text"))
    sort_controls((families))
    sorted_families = sort_parts(families)
    return sorted_families


def create_sortable_id(control_id, type: str = "simple"):
    if type == "simple":
        match = re.match(r"^([a-z]{2})-(\d+)$", control_id)
    else:
        match = re.match(r"^([a-z]{2})-(\d+)\s*\((\d+)\)$", control_id)
    if match:
        family = match.group(1)
        number = int(match.group(2))
        extension = f".{int(match.group(3))}" if type == "extended" else ""
        return f"{family.upper()}-{str(number).zfill(2)}{extension}"


def write_files(families: dict, out_dir: Path):
    """
    Write the Control Family data to markdown files.

    :param families: a dictionary of Controls sorted by Control Family.
    :param out_dir: a pathlib file path object where to write the files.
    """

    for family, controls in families.items():
        family_name = family[3:].replace("-", " ").title()
        filename = out_dir.joinpath(f"sop-{family}").with_suffix(".md")
        title = f"{family_name} ({family[:2].upper()}) Standard (SOP)"
        text = SopWriter(
            filepath=filename,
            controls=controls,
            title=title,
        )
        text.create_file()


@click.command()
@click.option(
    "--components",
    "-c",
    "components_dir",
    required=True,
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    help="Rendered components directory",
)
@click.option(
    "--out",
    "-o",
    "output_dir",
    type=click.Path(exists=False, dir_okay=True, readable=True),
    default=".",
    help="Output directory (default: current directory)",
)
def main(components_dir: str, output_dir: str):
    out_dir = Path(output_dir).joinpath("sop")
    if not out_dir.is_dir():
        out_dir.mkdir(parents=True, exist_ok=True)

    rendered_components = Path(components_dir)

    families = aggregate_control_data(rendered_components)

    write_files(families, out_dir)


def sort_parts(families: dict) -> dict:
    """
    Sort the Control Parts so that they are ordered alphabetically.

    :param families: a dictionary of Controls sorted by Control Family.
    :return: the control families dictionary with the parts sorted.
    """
    for family, control in families.items():
        """"""
        for control_id, parts in control.items():
            families[family][control_id] = {
                key: value for key, value in sorted(parts.items())
            }

    return families


def sort_controls(families: dict) -> dict:
    """
    Sort the Control Parts so that they are ordered alphabetically.

    :param families: a dictionary of Controls sorted by Control Family.
    :return: the control families dictionary with the parts sorted.
    """
    for family, control in families.items():
        families[family] = {key: value for key, value in sorted(control.items())}

    return families


if __name__ == "__main__":
    main()
