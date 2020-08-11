#!/usr/bin/env python

import openpyxl
import yaml
from pathlib import Path
from shutil import copyfile

def main():
    config = load_options()
    if file_exists(config['original_file']):
        dir_exists(config['copy_to_directory'])
        original = Path(config['original_file'])
        out = Path(config['copy_to_directory']).joinpath(original.name)
        print("Copying {} to {}".format(original, out))
        copyfile(original, out)

        sheet = config['sheet_name']
        start_row = config['starting_row']
        status_col = config['status_column']
        type_col = config['control_type_column']
        imp_col = config['implementation_column']
        control_col = config['control_column']

        st = get_statuses('keys/status.yaml')
        wb = openpyxl.load_workbook(filename=out, data_only=True)
        ws = wb[sheet]
        for key, row in enumerate(ws.iter_rows(min_row=start_row)):
            row_num = key + start_row
            if row[control_col].value is None:
                break
            ctrl = row[control_col].value
            status_key = ctrl.replace('(', '_(').replace('-0', '-')
            print(status_key)
            if status_key in st:
                print('Writing values...')
                ws[status_col+str(row_num)] = st[status_key]["implementation_status"]
                narrative = get_narratives(st[status_key]['summary'])
                ws[imp_col+str(row_num)] = narrative
            else:
                ws[status_col+str(row_num)] = 'not applicable'
        wb.save(out)
        wb.close()

def load_options():
    options_file = Path('keys/spreadsheet.yaml')
    if options_file.is_file():
        with open (options_file, newline="") as stream:
            options = yaml.safe_load(stream)
            return options
    else:
        create_options()

def file_exists(file):
    try:
        Path(file).exists()
    except FileNotFoundError as e:
        print(e)
    return True

def dir_exists(dir):
    '''Check that a directory exists. Create it if it doesn't.'''
    newdir = Path(dir)
    if not newdir.exists():
        newdir.mkdir(parents=True)

def get_statuses(status):
    if file_exists(status):
        st = Path(status)
        with open(st, "r", newline="") as stream:
            try:
                statuses = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return statuses

def get_narratives(summary):
    narrative = {}
    text = ''
    for key, c in summary.items():
        for s in c:
            if 'key' in s:
                if s['key'] not in narrative:
                    narrative[s['key']] = []
                narrative[s['key']].append({'name': key, 'summary': s['text']})
            else:
                text = text + s['text'] + '\n\r\n\r'

    if narrative:
        for key, n in narrative.items():
            text = '({})\n\r'.format(key)
            for t in n:
                text = text + t['name'] + ' provide\n\r' + t['summary'] + '\n\r'

    return text

def create_options():
    opts = {
        'original_file': '',
        'copy_to_directory': '',
        'sheet_name': '',
        'control_type_column': '',
        'status_column': '',
        'implementation_column': '',
        'starting_row': 1
    }
    dir_exists('keys')

    with open (Path('keys/spreadsheet.yaml'), mode='w', newline='\r\n') as opt_file:
        print('Creating keys/spreadsheet.yaml file.')
        yaml.dump(opts, opt_file)
    raise Exception('The values in the spreadsheet.yaml file are required.')

if __name__ == "__main__":
    main()