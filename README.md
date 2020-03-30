# Compliance Tools

## Overview

**Compliance Tools** is a suite of tools that facilitate the creation of system specific compliance documentation. For example, these tools may be used to generate a _System Security Plan_ (SSP) which is a necessary component of an _Authority to Operate_ (ATO) for federal systems.

Currently there are six tools; `createfiles`, `makefamilies`, `makessp`, `creatematrix`, `selectcontrols` and `exportto`. These tools are generally wrapped in a docker container for ease of deployment and use, e.g., [drydockcloud/ci-compliancetools](https://github.com/drydockcloud/ci-compliancetools).

### createfiles

`createfiles` generates the System Security Plan front matter, component files and appendices from templates and yaml data files using the [secrender](https://github.com/CivicActions/secrender) tool for variable replacement. The command can take three arguments; `in`, `out`, and `template`:

```bash
$ createfiles --help
Usage: createfiles.py [OPTIONS]

Options:
  -i, --in FILE              Replacement data values (YAML)  [required]
  -t, --templates DIRECTORY  Template directory  [required]
  -o, --out PATH             Output directory (default: current directory)
  --help                     Show this message and exit.
```

The output directory structure will mirror that found in the templates directory. For example, the following command will result in a file existing at `./templates/appendices/configuration-management.md.j2` to be _secrendered_ using the data file `config.yaml` and output to `./appendices/configuration-management.md`. (Note that the optional `.j2` suffix is removed.)

```bash
createfiles -i config.yaml -t templates
```

*A note about the replacement data values:* This file can include files from a different YAML file for cleaner, more concise files. For example, the line `project: !include keys/project.yaml` may include project specific information, keyed as `project` from the `keys/` directory.

### makefamilies

`makefamilies` aggregates the control files in the `components` directory by family, for example the file `docs/controls/AC.md` will contain all of the component controls that pertain to _Access Control_.

```bash
$ makefamilies --help
Usage: makefamilies [OPTIONS]

Options:
  -o, --out PATH  Output directory (default: ./docs/controls)
  --help          Show this message and exit.
```

### makessp

`makessp` simply aggregates all the control families into a single file: `docs/ssp.md`

### creatematrix

`creatematrix` generates a **responsiblity matrix** spreadsheet based on the components generated using `createfiles`. The spreadsheet shows the status of controls such as _In Place_, _Planned_, _Inherited_, etc, and which component is implementing those controls.

Usage:

```bash
$ creatematrix --help
Usage: creatematrix.py [OPTIONS]

Options:
  -i, --in DIRECTORY        The path to the components directory
                            (default: ./components)
  -c, --cert CERTIFICATION  The certification to use to create the matrix
                            (default: fisma-low-impact)
  --help                    Show this message and exit.
```

Note that the certification can be any of those defined in [OpenControl/Certifications](https://github.com/opencontrol/certifications).

### selectcontrols

`selectcontrols` recursively copies one OpenControl directory tree to
another, applying a filter to select particular controls.

The controls currently must be in a CivicActions modified format that extends the OpenControl
schema by supporting family controls to be grouped in separate files.
Files named `component.yaml` are copied without change.
Family files are copied and edited according to the selection filter.

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
$ selectcontrols --help
Options:
  -s, --selection FILENAME  selected controls (YAML)
  -i, --in DIRECTORY        Input directory tree  [required]
  -o, --out PATH            Output directory [defaults to current directory]
  -V, --verbose
  --help                    Show this message and exit.
```

### exportto

`exportto` *(in development)* enables creation of (e.g.) docx files generated from markdown files. Try:

```bash
exportto -c docs/controls
```

## Major Contributors

* **Fen Labalme** - [openprivacy](https://github.com/openprivacy)
* **Tom Camp** - [Tom-Camp](https://github.com/Tom-Camp)
* **Tom Wood** - [Woodt](https://github.com/woodt)

## License

This project is licensed under the GNU General Public License version 3 or any later version - see the [LICENSE](LICENSE) file for details. Some portions of this code are dedicated to the public domain under the terms of the Creative Commons Zero v1.0 Universal.

SPDX-License-Identifier: `GPL-3.0-or-later`

## Copyright

Copyright 2019-2020 CivicActions, Inc.
