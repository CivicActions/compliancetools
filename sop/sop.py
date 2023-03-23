#!/usr/bin/env python

from pathlib import Path

import click
import yaml  # type: ignore
from sop_writer import SopWriter

# Copyright 2019-2020 CivicActions, Inc. See the README file at the top-level
# directory of this distribution and at https://github.com/CivicActions/compliancetools#copyright.
#


def aggregate_control_data(component_dir: Path) -> dict:
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
            control_key = control.get("control_key")
            control_name = control.get("control_name").title()
            key = f"{control_key} {control_name}"
            if key and key not in families[family]:
                families[family][key] = {}

            for parts in control.get("narrative"):
                part = parts.get("key", "text")

                if part not in families[family][key]:
                    families[family][key][part] = []
                families[family][key][part].append(parts.get("text"))

    sorted_families = sort_parts(families)
    return sorted_families


def write_files(families: dict, out_dir: Path):
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
def main(components_dir: Path, output_dir: Path):
    out_dir = Path(output_dir).joinpath("sop")
    if not out_dir.is_dir():
        out_dir.mkdir(parents=True, exist_ok=True)

    rendered_components = Path(components_dir)

    families = aggregate_control_data(rendered_components)

    write_files(families, out_dir)


def sort_parts(families: dict) -> dict:
    for family, control in families.items():
        """"""
        for control_id, parts in control.items():
            families[family][control_id] = {
                key: value for key, value in sorted(parts.items())
            }

    return families


if __name__ == "__main__":
    main()
