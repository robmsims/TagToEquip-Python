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
    max_count = 2000000 # limit read in while testing
    top_schema = find_equip_and_tree.read_in_schema(file_name, loc_tagname, max_count)
    print('schema = {}'.format(top_schema))

    # get position of equipment type
    mode = 1 # ichr area designation
    percent_filter = 92
    data_base = find_equip_and_tree.find_equip_type_position_and_import_data(
        file_name, loc_tagname, max_count, top_schema, mode, percent_filter)
    schema_equip_position = data_base[0][0]
    print('equipment is located at word {} in the schema'.format(schema_equip_position))

    # is 2 chr mode needed
    first_level_tree = data_base[0][1]
    if first_level_tree < 0: # try 2ch mode
        mode = 2 # ichr area designation
        percent_filter = 98
        data_base = find_equip_and_tree.find_equip_type_position_and_import_data(
            file_name, loc_tagname, max_count, top_schema, mode, percent_filter)
        schema_equip_position = data_base[0][0]
        print('equipment is located at word {} in the schema'.format(schema_equip_position))

    # get area hierachey
    if not first_level_tree < 0:
        percent_filter = 90
        data_base = find_equip_and_tree.find_tree(file_name, top_schema, data_base,
                                              loc_tagname, max_count, mode, percent_filter)


if __name__ == '__main__':
    # This is executed when called from the command line nloc_iodevot repel
    try:
        file_name = sys.arg[1] # The 0th arg is the module file name.
    except:
        file_name = ''

    main(file_name)