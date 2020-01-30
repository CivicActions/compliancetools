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

### createssp

Once you have generated the _Control Families_ and the _front matter_, you can generate a markdown version of the _SSP_ using `makessp`. The `ssp.md` file will be created in the _docs/_ directory in the root of your project.

## License

This project is licensed under the GNU General Public License - see the [LICENSE](LICENSE) file for details.
