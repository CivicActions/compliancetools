#!/usr/bin/env python

# Copyright 2019-2020 CivicActions, Inc. See the README file at the top-level
# directory of this distribution and at https://github.com/CivicActions/compliancetools#copyright.

import os
from pathlib import Path

import click
import pypandoc


@click.command()
@click.option('--controls', '-c', 'control_dir',
              required=True,
              type=click.Path(exists=True, dir_okay=True, readable=True),
              help='The directory containing the control markdown files')
@click.option('--type', '-t', 'file_type',
              required=False,
              default='docx',
              help='The file type to create using Pandoc (default: docx)')
@click.option('--out', '-o', 'out_',
              type=click.Path(exists=False, dir_okay=True, readable=True),
              default='docx',
              help='Output directory (default: docx)')
def main(control_dir, file_type, out_):
  base_path = Path()
  output_dir = base_path.joinpath(out_)
  if not output_dir.exists():
    os.mkdir(output_dir)

  dirpath = Path(control_dir)
  try:
    dirpath_abs = dirpath.resolve(strict=True)
  except FileNotFoundError as e:
    print(e)

  args = []
  if file_type == 'docx':
    if Path('assets/custom-reference.docx').exists():
      args.append('--reference-doc=assets/custom-reference.docx')


  for x in dirpath.iterdir():
    if x.is_file() and x.suffix == '.md':
      outfile = output_dir.joinpath(x.stem+'.'+file_type)
      print("Creating file {}".format(outfile))
      output = pypandoc.convert_file(
        str(x),
        file_type,
        outputfile=str(outfile),
        extra_args=args
      )

if __name__ == '__main__':
    main()
