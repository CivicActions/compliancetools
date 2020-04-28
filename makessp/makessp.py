#!/usr/bin/env python

# Copyright 2019-2020 CivicActions, Inc. See the README file at the top-level
# directory of this distribution and at https://github.com/CivicActions/compliancetools#copyright.

import os
from grc import ssp
from grc import opencontrol
import md_toc
from pathlib import Path

def main():
    parent = Path()
    docs = parent.joinpath('docs')
    if not docs.exists():
      os.mkdir(docs)

    try:
        oc_yaml_abs = parent.joinpath("opencontrol.yaml").resolve(strict=True)
    except FileNotFoundError:
        print("No opencontrol.yaml file!")

    project = opencontrol.load_project_from_path(parent)
    ssp_doc = parent.joinpath(docs, 'ssp.md')
    with open(ssp_doc, 'w', newline="") as output:
      # Table of Contents placeholder.
      print('<!--TOC-->\n\n', file=output)
      # Create SSP document.
      print(ssp.build_ssp(project, {
        "include-control-descriptions": True,
      }), file=output)

    # Make the Table of Contents placeholder.
    toc = md_toc.build_toc(ssp_doc, keep_header_levels=2, skip_lines=2)
    md_toc.write_string_on_file_between_markers(ssp_doc, toc, '<!--TOC-->')

if __name__ == '__main__':
    main()
