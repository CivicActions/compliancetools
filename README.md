# Compliance Tools

## Overview

**Compliance Tools** is a suite of tools used to generate a _System Security Plan_. Currently there are three tools; `makefamilies`, `makefiles`, and `createssp`.

### makefamilies

`makefamilies` is used to aggregate the control files by family, for example the file **AC.md** would contain all of the controls that pertain to _Access Control_. For example, it might contain the controls that are covered by _AWS_, the _contractor_, and the _application_.

### createfiles

`createfiles` is used to up

Example:
`createfiles -i config.yaml -o docs -t templates`

```bash
Usage: createfiles.py [OPTIONS]

Options:
  -i, --in FILE        values (YAML)  [required]
  -o, --out PATH       Output directory  [required]
  -t, --template PATH  Template directory  [required]
  --help               Show this message and exit.
```
