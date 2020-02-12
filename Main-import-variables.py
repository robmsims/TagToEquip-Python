#!/usr/bin/env python3
"""Retrive and print schema from a fime

Usage:
    python3 Main-import-variables.py filename eg D:\Import\Site1\variable.csv
"""
import sys
import find_equip_and_tree


def main(file_name = ''):
    if file_name == '':
        file_name = 'D:\\Import\\Site1\\variable.csv'  # set a default file name

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
    max_count = 2000000  # limit read in while testing
    top_schema = find_equip_and_tree.read_in_schema(file_name, loc_tagname, max_count)
    print('schema = {}'.format(top_schema))

    # get position of equipment type
    mode = 1  # 1 character area designation
    percent_filter = 92
    data_base = find_equip_and_tree.find_equip_type_position_and_import_data(
                    file_name, loc_tagname, max_count, top_schema, mode, percent_filter)
    schema_equip_position = data_base[0][0]
    print('equipment is located at word {} in the schema'.format(schema_equip_position))

    # is 2 character mode needed
    first_level_tree = data_base[0][1]
    if first_level_tree < 0: # try 2ch mode
        mode = 2  # chr area designation
        percent_filter = 98
        data_base = find_equip_and_tree.find_equip_type_position_and_import_data(
                        file_name, loc_tagname, max_count, top_schema, mode, percent_filter)
        schema_equip_position = data_base[0][0]
        print('equipment is located at word {} in the schema'.format(schema_equip_position))

    # get area hierachey
    if first_level_tree >= 0:
        filter = 90
        data_base = find_equip_and_tree.find_tree(file_name, top_schema, data_base,
                                    loc_tagname, max_count, mode, filter, percent_filter)

    # sanitise area list order
    first_level_tree = data_base[0][1]
    second_level_tree = data_base[0][2]
    if second_level_tree >= 0:
        if second_level_tree < first_level_tree:
            # re read and make second_level_tree  => first_level_tree
            data_base = find_equip_and_tree.find_equip_type_position_and_import_data(
                    file_name, loc_tagname, max_count, top_schema, mode, percent_filter)
            data_base[0][1] = second_level_tree
            # get area hierachey again
            filter = 90
            data_base = find_equip_and_tree.find_tree(file_name, top_schema, data_base,
                                    loc_tagname, max_count, mode, filter, percent_filter)

    first_level_tree = data_base[0][1]
    second_level_tree = data_base[0][2]
    third_level_tree = data_base[0][3]
    fourth_level_tree = data_base[0][4]

    if fourth_level_tree < third_level_tree:
        fourth_level_tree = -1

    if third_level_tree < second_level_tree:
        third_level_tree = -1
        fourth_level_tree = -1

    if second_level_tree < first_level_tree:
        second_level_tree = -1
        third_level_tree = -1
        fourth_level_tree = -1

    # sanitise area list spaceing
    area_spaceing = second_level_tree - first_level_tree
    if area_spaceing < third_level_tree - second_level_tree:
        third_level_tree = -1
        fourth_level_tree = -1

    if area_spaceing < fourth_level_tree - third_level_tree:
        fourth_level_tree = -1

    # print final tree
    #print('---- final tree order')
    if first_level_tree >= 0:
        print('first level is at schema position {}'.format(first_level_tree+1))  # convert to 1 base
    if second_level_tree>= 0:
        print('second level is at schema position {}'.format(second_level_tree+1))  # convert to 1 base
    if third_level_tree >= 0:
        print('third level is at schema position {}'.format(third_level_tree+1))  # convert to 1 base
    if fourth_level_tree >= 0:
        print('fourth level is at schema position {}'.format(fourth_level_tree+1))  # convert to 1 base

    # find the item name
    # re read in equipment
    data_base[0][1] = first_level_tree
    data_base[0][2] = second_level_tree
    data_base[0][3] = third_level_tree
    data_base[0][4] = fourth_level_tree

    data_base, is_item_digits_found = find_equip_and_tree.find_item(file_name, loc_tagname,
                                                            max_count, top_schema, data_base, mode)

    if is_item_digits_found:
        last_digit = data_base[0][5]
        first_digit = data_base[0][6]
        print('item found last digit position {}, first digit position {}'
                                                            .format(last_digit+1, first_digit+1))


if __name__ == '__main__':
    # This is executed when called from the command line nloc_iodevot repel
    try:
        file_name = sys.arg[1]  # The 0th arg is the module file name.
    except:
        file_name = ''

    main(file_name)