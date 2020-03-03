# Compliance Tools

## Overview

**Compliance Tools** is a suite of tools used to generate a _System Security Plan_. Currently there are three tools; `makefamilies`, `makefiles`, and `createssp`.

### makefamilies

`makefamilies` is used to aggregate the control files by family, for example the file `AC.md` would contain all of the controls that pertain to _Access Control_. For example, it might contain the controls that are covered by _AWS_, the _contractor_, and the _application_.

### createfiles

`createfiles` is used to generate the appendices and the component files to be used in the creation of the `ssp.md` file. The command can take three arguments; `in`, `out`, and `template`.

`createfiles` will create the files, using the same directory structure that is contained within the `--templates` directory. For example, if you have a file named _configuration-management.md.j2_ within the `templates/appendices`, if you pass `-t templates` as the template argument, `createfiles` will create a directory name `appendices` in the root of your project and the file `configuration-management.md` in that directory.

Example:
`createfiles -i config.yaml -o docs -t templates`

`in`, `-i`, `--in`, ***this argument is required*** - This is a YAML file that contains the variables that will be used to replace placeholders in the templates. This file can include files from a different YAML file for cleaner, more concise files, for example `project: !include keys/project.yaml` would inlcude project specific information, keyed as `project` from the `keys/` directory.

`out`, `-o`, `--out` - A path where to output the generated files.

`template`, `-t`, `--template` ***this argument is required*** - A path to a directory containing the template files.

```bash
Usage: createfiles.py [OPTIONS]

Options:
  -i, --in FILE        values (YAML)  [required]
  -o, --out PATH       Output directory  [required]
  -t, --template PATH  Template directory  [required]
  --help               Show this message and exit.
```

### makessp

Once you have generated the _Control Families_ and the _front matter_, you can generate a markdown version of the _SSP_ using `makessp`. The `ssp.md` file will be created in the _docs/_ directory in the root of your project.

### creatematrix

`creatematrix` will generate a **responsiblity matrix** spreadsheet based on the components generated using createfiles. The spreadsheet shows the status of components such as _In Place_, _Planned_, _Inherited_, etc, and who is implementing those components.

Example:
`creatematrix --in components --cert fisma-low-impact`

`-i`, `--in` - This is the path to the components directory. This will default to `./components/` if no option is provided.

`-c`, `--cert` - Define what _certification_ to use to generate the matrix. If not provided, this will default to `fisma-low-impact`.

```bash
Usage: creatematrix.py [OPTIONS]

Options:
  -i, --in DIRECTORY              The path to the components directory.
  -c, --cert [dhs-4300a|fedramp-high|fedramp-low|fedramp-moderate|fedramp-tailoredfisma-high-impact|fisma-low-impact|fisma-moderate-impact|icd-503-high|icd-503-low|icd-503-moderate]
                                  The certification to use to create the
                                  matrix.
  --help                          Show this message and exit.
```

## Major Contributors

* **Tom Wood** - *Initial work* - [Woodt](https://github.com/woodt)
* **Tom Camp** - [Tom-Camp](https://github.com/Tom-Camp)

## License

This project is licensed under the GNU General Public License version 3 or any later version - see the [LICENSE](LICENSE) file for details. Some portions of this code are dedicated to the public domain under the terms of the Creative Commons

## Copyright

Copyright 2019-200 CivicActions, Inc.
