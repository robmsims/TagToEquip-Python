#!/usr/bin/env python3
"""Retrive and print schema from a fime

Usage:
    python3 Main-import-variables.py filename    eg D:\Import\Site1\variable.csv
"""
import sys
import find_equip_and_tree
import read_in_tree_structure
import os.path
import write_read_config_file
import encode_decode_map_schema


def update_csv_files(file_path, config_file):
    map_schema, area_map, equipment_map_dict = write_read_config_file.read_config_file(config_file)
    equip_list = read_in_tree_structure.update_tag_csvs(map_schema, area_map, file_path)

    read_in_tree_structure.update_equipment_csv(file_path, equip_list)

    read_in_tree_structure.replace_original_csv(file_path)


def get_schema_and_create_config_file(file_path, config_file):
    file_name = file_path + "\\variable.csv"

    # get header file
    header = read_in_tree_structure.read_first_line(file_name)

    loc_tagname = header.index('tag name')
    loc_cluster = header.index('cluster name')

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
    if first_level_tree < 0:  # try 2ch mode
        mode = 2  # chr area designation
        percent_filter = 98
        data_base = find_equip_and_tree.find_equip_type_position_and_import_data(
                        file_name, loc_tagname, loc_cluster, max_count, top_schema, mode, percent_filter)

    # get area hierachey
    if first_level_tree >= 0:
        score_filter = 90
        data_base = find_equip_and_tree.find_tree(file_name, top_schema, data_base, loc_tagname, loc_cluster,
                                                  max_count, mode, score_filter, percent_filter)

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
            score_filter = 90
            data_base = find_equip_and_tree.find_tree(file_name, top_schema, data_base, loc_tagname, loc_cluster,
                                                      max_count, mode, score_filter, percent_filter)

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
    area_spacing = second_level_tree - first_level_tree
    if area_spacing < third_level_tree - second_level_tree:
        third_level_tree = -1
        fourth_level_tree = -1

    if area_spacing < fourth_level_tree - third_level_tree:
        fourth_level_tree = -1

    # find the item name
    # -re read in equipment
    data_base[0][1] = first_level_tree
    data_base[0][2] = second_level_tree
    data_base[0][3] = third_level_tree
    data_base[0][4] = fourth_level_tree

    # - create a map schema
    data_base, is_item_found = find_equip_and_tree.find_item(file_name, loc_tagname, loc_cluster,
                                                             max_count, top_schema, data_base, mode)
    first_level_tree = data_base[0][1]
    second_level_tree = data_base[0][2]
    third_level_tree = data_base[0][3]
    fourth_level_tree = data_base[0][4]

    if is_item_found:
        last_digit = data_base[0][5]
        print('item found from position {}'.format(last_digit + 1))

        # print final tree
        print('first level is at schema position {}'.format(first_level_tree + 1))  # convert to 1 base
        if second_level_tree >= 0:
            print('second level is at schema position {}'.format(second_level_tree + 1))  # convert to 1 base
        if third_level_tree >= 0:
            print('third level is at schema position {}'.format(third_level_tree + 1))  # convert to 1 base
        if fourth_level_tree >= 0:
            print('fourth level is at schema position {}'.format(fourth_level_tree + 1))  # convert to 1 base

        # generate map schema
        matrix0 = data_base[0]
        map_schema = encode_decode_map_schema.encode_mapping_schema(matrix0, mode, top_schema)

        # generate config file
        print('----- creating mapping file at path given -----')
        print('map schema {}'.format(map_schema))

        # - create an equipment tree based on found schema so we can create a file for mapping
        data_base = read_in_tree_structure.get_equipment_tree(file_name, loc_tagname, loc_cluster,
                                                              max_count, map_schema)

        equipment_list = sorted(data_base[1][0])
        write_read_config_file.write_config(config_file, map_schema, equipment_list)
        print('Default config file writen')


def main(file_path=''):
    if file_path == '':
        file_path = 'D:\\Import\\example'  # set a default file name
        print('argument not entered. using default {}'.format(file_path))

    config_file = file_path + "\\mapping.ini"

    config_file_exists = os.path.isfile(config_file)
    if not config_file_exists:
        get_schema_and_create_config_file(file_path, config_file)
    else:
        update_csv_files(file_path, config_file)


if __name__ == '__main__':
    # This is executed when called from the command line nloc_iodevot repel
    try:
        project_file_path = sys.argv[1]  # The 0th arg is the module file name.
    except IndexError as error:
        project_file_path = ''

    main(project_file_path)
