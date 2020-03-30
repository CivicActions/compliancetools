# Compliance Tools

## Overview

**Compliance Tools** is a suite of tools used to generate a _System Security Plan_, (SSP) a necessary component of an _Authority to Operate_ (ATO) for federal systems. Currently there are six tools; `createfiles`, `makefamilies`, `makessp`, `creatematrix`, `selectcontrols` and `exportto`.

These compliance tools are generally employed when wrapped in a docker container, e.g.,  using [drydockcloud/ci-compliancetools](https://github.com/drydockcloud/ci-compliancetools).

### createfiles

`createfiles` generates the System Security Plan front matter, component files and appendices from templates and yaml data files using the [secrender](https://github.com/CivicActions/secrender) tool for variable replacement. The command can take three arguments; `in`, `out`, and `template`:

```bash
$ createfiles --help
Usage: createfiles.py [OPTIONS]

Options:
  -i, --in FILE              values (YAML)  [required]
  -t, --templates DIRECTORY  Template directory  [required]
  -o, --out PATH             Output directory (defaults to current directory)
  --help                     Show this message and exit.
```

The output directory structure will mirror that found in the templates directory. For example, the following command will result in a file existing at `templates/appendices/configuration-management.md.j2` to be _secrendered_ using the data file `config.yaml` and output to `appendices/configuration-management.md`. (Note that the optional `.j2` suffix is removed.)

```bash
createfiles -i config.yaml -t templates
```

A note about the input data values: This file can include files from a different YAML file for cleaner, more concise files. For example, the line `project: !include keys/project.yaml` may include project specific information, keyed as `project` from the `keys/` directory.

### makefamilies

`makefamilies` aggregates the control files in the `components` directory by family, for example the file `docs/controls/AC.md` will contain all of the component controls that pertain to _Access Control_.

### makessp

`makessp` simply aggregates all the control families into a single file: `docs/ssp.md`

### creatematrix

`creatematrix` generates a **responsiblity matrix** spreadsheet based on the components generated using `createfiles`. The spreadsheet shows the status of components such as _In Place_, _Planned_, _Inherited_, etc, and who is implementing those components.

Example:
`creatematrix --in components --cert fisma-low-impact`

`-i`, `--in` - This is the path to the components directory (default: `./components/`).

`-c`, `--cert` - Define what _certification_ to use to generate the matrix (default: `fisma-low-impact`).

```bash
$ creatematrix --help
Usage: creatematrix.py [OPTIONS]

Options:
  -i, --in DIRECTORY              The path to the components directory.
  -c, --cert [dhs-4300a|fedramp-high|fedramp-low|fedramp-moderate|fedramp-tailored|fisma-high-impact|fisma-low-impact|fisma-moderate-impact|icd-503-high|icd-503-low|icd-503-moderate]
                                  The certification to use to create the
                                  matrix.
  --help                          Show this message and exit.
```

### selectcontrols

`selectcontrols` recursively copies one OpenControl directory tree to
another, applying a filter to select particular controls.

The controls must be in Fen-format.  Files named `component.yaml` are
copied without change.  Family files are copied and edited according
to the selection filter.

The selection filter is a YAML file in the OpenControl certification format.

Example selection file:

```yaml
-- Controls selected for limited scope assessment
name: Limited Scope Assessment
standards:
  NIST-800-53 rev4:
    AC-1:
    AC-2:
    CM-2:
    CM-4:
    IR-2:
    IR-8:
  NIST SP 800-53 Revision 4 Privacy:
    AP-2:
```

Example usage:

```bash
$ selectcontrols --in components --out Limited_Scope --selection lsa.yaml
```

Usage:
```
Options:
  -s, --selection FILENAME  selected controls (YAML)
  -i, --in DIRECTORY        Input directory tree  [required]
  -o, --out PATH            Output directory [defaults to current directory]
  -V, --verbose
  --help                    Show this message and exit.
```

### exportto

`exportto` *(in development)* enables creation of (e.g.) docx files generated from markdown files. 

## Major Contributors

* **Fen Labalme** - [openprivacy](https://github.com/openprivacy)
* **Tom Camp** - [Tom-Camp](https://github.com/Tom-Camp)
* **Tom Wood** - [Woodt](https://github.com/woodt)

## License

This project is licensed under the GNU General Public License version 3 or any later version - see the [LICENSE](LICENSE) file for details. Some portions of this code are dedicated to the public domain under the terms of the Creative Commons Zero v1.0 Universal.

SPDX-License-Identifier: `GPL-3.0-or-later`

## Copyright

Copyright 2019-2020 CivicActions, Inc.
