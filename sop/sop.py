#!/usr/bin/env python

from pathlib import Path

import click
import yaml  # type: ignore

# Copyright 2019-2020 CivicActions, Inc. See the README file at the top-level
# directory of this distribution and at https://github.com/CivicActions/compliancetools#copyright.
#


@click.command()
@click.option(
    "--in",
    "-i",
    "input_file",
    required=True,
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help="Replacement data values (YAML)",
)
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
def main(input_file: Path, components_dir: Path, output_dir: Path):
    out_dir = Path(output_dir)
    if not out_dir.is_dir():
        out_dir.mkdir(parents=True, exist_ok=True)
    rendered_components = Path(components_dir)
    if rendered_components.resolve():
        families: dict = {}
        components = rendered_components.rglob("*")
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
                key = control.get("control_key")
                if key and key not in families[family]:
                    families[family][key] = {}

                for parts in control.get("narrative"):
                    part = parts.get("key", "text")

                    if part not in families[family][key]:
                        families[family][key][part] = []
                    families[family][key][part].append(parts.get("text"))

    sort_parts(families)
    print(families)


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
