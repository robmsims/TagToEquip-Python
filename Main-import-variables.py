#!/usr/bin/env python3
"""Retrive and print schema from a fime

Usage:
    python3 Main-import-variables.py filename eg D:\Import\Site1\variable.csv
"""
import sys
import read_csv_file

def read_in_schema(file_name, loc_tagname, max_count):
    data_block = []
    with open(file_name, mode='rt', encoding='utf-8') as f:
        read_count = 0
        for read_line in f:
            if read_count > 0:
                tag = read_csv_file.read_in_data(loc_tagname, read_line.strip())
                g_tag = [] # not used here but required by function get_schema
                current_schema = read_csv_file.get_schema(tag, g_tag)
                data_block.append(current_schema)

            read_count += 1
            if read_count > max_count:
                break

    last_schema = ''
    top_count = 0
    data_block.sort()
    for current_schema in data_block:
        if not last_schema == current_schema:
            count = 0 # reset count on change of schema

        last_schema = current_schema
        count += 1
        if count > top_count:
            top_count = count
            schema = current_schema

    return schema


def read_first_line(file_name):
    with open(file_name, mode='rt', encoding='utf-8') as f:
        return f.readline().strip().lower().rsplit(',')


def main(file_name = ''):
    if file_name == '':
        file_name = 'D:\\Import\\Site1\\variable.csv' # set a default file name

    header = read_first_line(file_name)
    loc_equip = header.index('equipment')
    loc_item = header.index('item name')
    loc_tagname = header.index('tag name')
    loc_iodev = header.index('i/o device')

    print(header)
    print('Equipment loation {}'.format(loc_equip))
    print('Equipment Item location {}'.format(loc_item))
    print('Tag Name {}'.format(loc_tagname))
    print('Equipment I/O Device {}'.format(loc_iodev))

    max_count = 200000 # limit read in while testing
    top_schema = read_in_schema(file_name, loc_tagname, max_count)
    print('schema = {}'.format(top_schema))


if __name__ == '__main__':
    # This is executed when called from the command line nloc_iodevot repel
    try:
        file_name = sys.arg[1] # The 0th arg is the module file name.
    except:
        file_name = ''

    main(file_name)