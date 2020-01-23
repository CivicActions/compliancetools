#!/usr/bin/env python

from os import path, mkdir
import ssp, opencontrol
import md_toc

def main():
    parent = path.abspath(path.dirname( __file__ ))
    docs = path.join(parent,'docs')
    if not path.exists(docs):
      mkdir(docs)

    project = opencontrol.load_project_from_path(parent)
    ssp_doc = path.join(docs, 'ssp.md')
    with open(ssp_doc, 'w') as output:
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
