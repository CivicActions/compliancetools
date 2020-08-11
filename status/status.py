#!/usr/bin/env python

import rtyaml
from pathlib import Path

def main():
    oc = get_opencontrol()
    component_files = []
    # Create a list of all of the components in the project.
    for component in oc['components']:
        p = Path(component).rglob("*")
        files = [x for x in p if x.is_file() and x.name != 'component.yaml']
        component_files.extend(files)
        component_files.sort()
    parse_controls(component_files)

def get_opencontrol():
    oc_yaml = Path('opencontrol.yaml')
    try:
        oc_yaml_abs = oc_yaml.resolve(strict=True)
    except FileNotFoundError:
        print("No opencontrol.yaml file!")

    try:
        with open(oc_yaml, encoding="utf8") as f:
            try:
                opencontrol = rtyaml.load(f)
            except Exception as e:
                raise ValueError("OpenControl {} file {} has invalid data (is not valid YAML: {}).".format(
                    schema_type,
                    fn,
                    str(e) ))
            if not isinstance(opencontrol, dict):
                raise ValueError("OpenControl {} file {} has invalid data (should be a mapping, is a {}).".format(
                    schema_type,
                    fn,
                    type(opencontrol) ))
    except IOError as e:
        raise ValueError("OpenControl {} file {} could not be loaded: {}.".format(
            schema_type,
            fn,
            str(e) ))
    return opencontrol

def parse_controls(comps):
    with open('keys/status.yaml', newline='') as st:
        stati = rtyaml.load(st)
    for c in comps:
        with open(c, newline='') as ct:
            component = rtyaml.load(ct)
            for s in component['satisfies']:
                key = str(s['control_key']).replace(' ', '_')
                if key in stati:
                    stati[key]['type'] = s['security_control_type']
                    narrative = get_narrative(s)
                    stati[key]['summary'][c.parent.name] = narrative
    with open('keys/status.yaml', mode='w', newline='') as st:
        rtyaml.dump(stati, st)

def get_narrative(control):
    narr = []
    for n in control['narrative']:
        p = {}
        if 'key' in n:
            p['key'] = n['key']
        p['text'] = n['text']
        narr.append(p)
    return narr

if __name__ == "__main__":
    main()