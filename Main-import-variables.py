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
    print(header)

    loc_equip = header.index('equipment')
    loc_item = header.index('item name')
    loc_tagname = header.index('tag name')
    loc_iodev = header.index('i/o device')
    loc_cluster = header.index('cluster name')
    print('Equipment loation {}'.format(loc_equip))
    print('Equipment Item location {}'.format(loc_item))
    print('Tag Name {}'.format(loc_tagname))
    print('Equipment I/O Device {}'.format(loc_iodev))
    print('Equipment Cluster {}'.format(loc_cluster))

    # get most common schema
    max_count = 2000000  # limit read in while testing
    top_schema = find_equip_and_tree.read_in_schema(file_name, loc_tagname, max_count)
    print('schema = {}'.format(top_schema))

    # get position of equipment type
    mode = 1  # 1 character area designation
    percent_filter = 92
    data_base = find_equip_and_tree.find_equip_type_position_and_import_data(
                    file_name, loc_tagname, loc_cluster, max_count, top_schema, mode, percent_filter)

    equip_level_tree = data_base[0][0]
    if equip_level_tree >= 0:
        print('equipment is located at position {} in the schema'.format(equip_level_tree + 1))

    # is 2 character mode needed
    first_level_tree = data_base[0][1]
    if first_level_tree < 0: # try 2ch mode
        mode = 2  # chr area designation
        percent_filter = 98
        data_base = find_equip_and_tree.find_equip_type_position_and_import_data(
                        file_name, loc_tagname, loc_cluster, max_count, top_schema, mode, percent_filter)

    # get area hierachey
    if first_level_tree >= 0:
        filter = 90
        data_base = find_equip_and_tree.find_tree(file_name, top_schema, data_base,
                                    loc_tagname, loc_cluster, max_count, mode, filter, percent_filter)

    #return  #  debug

    # sanitise area list order
    first_level_tree = data_base[0][1]
    second_level_tree = data_base[0][2]
    if second_level_tree >= 0:
        if second_level_tree < first_level_tree:
            # re read and make second_level_tree  => first_level_tree
            data_base = find_equip_and_tree.find_equip_type_position_and_import_data(
                    file_name, loc_tagname, loc_cluster, max_count, top_schema, mode, percent_filter)
            data_base[0][1] = second_level_tree
            # get area hierachey again
            filter = 90
            data_base = find_equip_and_tree.find_tree(file_name, top_schema, data_base,
                                    loc_tagname, loc_cluster, max_count, mode, filter, percent_filter)

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

    # find the item name
    # re read in equipment
    data_base[0][1] = first_level_tree
    data_base[0][2] = second_level_tree
    data_base[0][3] = third_level_tree
    data_base[0][4] = fourth_level_tree

    data_base, is_item_found = find_equip_and_tree.find_item(file_name, loc_tagname, loc_cluster,
                                                            max_count, top_schema, data_base, mode)
    equip_level_tree = data_base[0][0]
    first_level_tree = data_base[0][1]
    second_level_tree = data_base[0][2]
    third_level_tree = data_base[0][3]
    fourth_level_tree = data_base[0][4]

    if is_item_found:
        last_digit = data_base[0][5]
        print('item found from position {}'.format(last_digit+1))

        # print final tree
        print('first level is at schema position {}'.format(first_level_tree + 1))  # convert to 1 base
        if second_level_tree >= 0:
            print('second level is at schema position {}'.format(second_level_tree + 1))  # convert to 1 base
        if third_level_tree >= 0:
            print('third level is at schema position {}'.format(third_level_tree + 1))  # convert to 1 base
        if fourth_level_tree >= 0:
            print('fourth level is at schema position {}'.format(fourth_level_tree + 1))  # convert to 1 base

        # generate generic schema
        schema = ''
        if is_item_found:
            schema = top_schema

            if first_level_tree >= 0:
                schema = schema[0:first_level_tree] + "A" + schema[first_level_tree+1:]
                end_schema = first_level_tree
            if first_level_tree >= 0 and mode == 2:
                schema = schema[0:first_level_tree+1] + "a" + schema[first_level_tree+2:]
                end_schema = first_level_tree + 1

            if second_level_tree >= 0:
                schema = schema[0:second_level_tree] + "B" + schema[second_level_tree+1:]
                end_schema = second_level_tree
            if second_level_tree >= 0 and mode == 2:
                schema = schema[0:second_level_tree+1] + "b" + schema[second_level_tree+2:]
                end_schema = second_level_tree + 1

            if third_level_tree >= 0:
                schema = schema[0:third_level_tree] + "C" + schema[third_level_tree + 1:]
                end_schema = third_level_tree
            if third_level_tree >= 0 and mode == 2:
                schema = schema[0:third_level_tree + 1] + "c" + schema[third_level_tree + 2:]
                end_schema = third_level_tree + 1

            if fourth_level_tree >= 0:
                schema = schema[0:fourth_level_tree] + "D" + schema[fourth_level_tree + 1:]
                end_schema = fourth_level_tree
            if fourth_level_tree >= 0 and mode == 2:
                schema = schema[0:fourth_level_tree + 1] + "d" + schema[fourth_level_tree + 2:]
                end_schema = fourth_level_tree + 1

            schema = schema[0:equip_level_tree] + "E" + schema[equip_level_tree+1:]
            if equip_level_tree > end_schema:
                end_schema = equip_level_tree

            last_digit = data_base[0][5]
            if last_digit > end_schema:
                schema = schema[0:last_digit] + "I"
            else:
                schema = schema[0:last_digit] + "I" + schema[last_digit + 1:]
                schema = schema[0:end_schema+1]
                print('Warning item part start is before area digit')

        print(schema)


if __name__ == '__main__':
    # This is executed when called from the command line nloc_iodevot repel
    try:
        file_name = sys.arg[1]  # The 0th arg is the module file name.
    except:
        file_name = ''

    main(file_name)