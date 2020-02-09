#!/usr/bin/env python3
"""Retrive and print schema from a fime

Usage:
    python3 Main-import-variables.py filename eg D:\Import\Site1\variable.csv
"""
import sys
import find_equip_and_tree


def main(file_name = ''):
    if file_name == '':
        file_name = 'D:\\Import\\Site1\\variable.csv' # set a default file name

    # get header file
    header = find_equip_and_tree.read_first_line(file_name)
    loc_equip = header.index('equipment')
    loc_item = header.index('item name')
    loc_tagname = header.index('tag name')
    loc_iodev = header.index('i/o device')

    print(header)
    print('Equipment loation {}'.format(loc_equip))
    print('Equipment Item location {}'.format(loc_item))
    print('Tag Name {}'.format(loc_tagname))
    print('Equipment I/O Device {}'.format(loc_iodev))

    # get most common schema
    max_count = 24 # limit read in while testing
    top_schema = find_equip_and_tree.read_in_schema(file_name, loc_tagname, max_count)
    print('schema = {}'.format(top_schema))

    # get position of equipment type
    schema_equip_position = find_equip_and_tree.find_equip_type_position_and_import_data(
        file_name, loc_tagname, max_count, top_schema)
    print('equipment is located at position {} in the schema'.format(schema_equip_position))


if __name__ == '__main__':
    # This is executed when called from the command line nloc_iodevot repel
    try:
        file_name = sys.arg[1] # The 0th arg is the module file name.
    except:
        file_name = ''

    main(file_name)