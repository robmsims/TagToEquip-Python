#!/usr/bin/env python3
'''Retrieve and print schema from a variable.dbf file
    save a default config file
    process default config file on 2nd run writeing changes back to csv file
    Note: uses 3rd party library https://pypi.org/project/dbf/ to read in variable.dbf
    from terminal >pip install -r requirements.txt

Usage:
    python3 Main-import-variables.py filename  eg C:\\ProgramData\\Schneider Electric\\Citect SCADA 2018\\User\\Example
    --on 2nd run
    python3  Mail-import-variables {path}    --> read in mapping.ini under {path} and
    create *-working.csv files containing equipment field changes
    which can be imported into project using Citect Studio import
'''

import sys
import find_equip_and_tree
import read_in_tree_structure
import os.path
import write_read_config_file
import encode_decode_map_schema
import read_write_dbf
import read_write_project_structure
import friendly_name_lookup
import read_csv_file


def map_dbf_to_csv(file_path):
    print('Converting .dbf files to .csv files')

    # find master.dbf
    master_file_path = file_path[0:file_path.rfind('\\')]
    master_file = master_file_path + '\\master.dbf'

    # build know project name vs project path
    dbf_file_exists = os.path.isfile(master_file)
    if dbf_file_exists:
        master_list, _ = read_write_dbf.read_in_dbf(master_file)
        master_project_name = read_write_project_structure.find_name_for_path(master_list, file_path)

        # mark master project to be read for included projects
        master_list = read_write_project_structure.\
            write_field_value(master_list, master_project_name, 'include_read_in_status', 1)

        # make flat list of projects
        master_list = read_write_project_structure.read_through_include_files(master_list)
        project_list = list()
        for record in master_list:
            if record['include_read_in_status'][1] == 2:
                project_list.append(record['name'][1])

        print('-Include files read. list of projects to convert is {}'.format(project_list))

        # read in friendly name
        dbf_csv_lookup_dict = friendly_name_lookup.build_field_friendly_name_lookup(file_path)

        # export all dbf files to convert. csvs will be stored in master and include data from all includes projects
        # note system includes excluded
        read_write_dbf.convert_dbf_to_csv_in_project_list(master_list, project_list, file_path, dbf_csv_lookup_dict)

        print('Completed dbf export to csv files in master and include projects')


def update_csv_files(file_path, config_file):
    print('Updating csv files with new equipment references')
    print('- reading in mapping.ini file')
    map_schema, area_map, equipment_map_dict, equipment_type_map_dict, item_type_map_dict, area_prefix_map_dict = \
        write_read_config_file.read_config_file(config_file)

    # write to tag csvs and outut equip list
    equip_list = read_in_tree_structure.update_tag_csvs(map_schema, area_map, file_path, equipment_map_dict,
                                                    equipment_type_map_dict, item_type_map_dict, area_prefix_map_dict)

    # write to equip.csv
    read_in_tree_structure.update_equipment_csv(file_path, equip_list)

    # read_in_tree_structure.replace_original_csv(file_path)
    print('Update of csvs complete')

    # for dev purposes only
    # verify generated files header against exported files header ie *-citect.csv
    file_list = read_in_tree_structure.get_file_list()
    for csv_file_name in file_list:
        citect_file = csv_file_name[0:csv_file_name.rfind('.')] + '-citect.csv'
        if os.path.isfile(file_path + '\\' + citect_file):
            print('-searching for header match for file {}'.format(csv_file_name))
            header_is_valid = read_csv_file.test_compare_file_headers(file_path, csv_file_name, citect_file)
            if header_is_valid:
                header_is_valid = read_csv_file.test_compare_file_headers(file_path, citect_file, csv_file_name)

            if header_is_valid:
                print('----file {} is valid'.format(csv_file_name))

    print('Ready to import csv files in master project folder using Citect Studio import feature')


def get_schema_and_create_config_file(file_path, config_file):
    print('Building Equipment Schema')
    file_name = file_path + "\\variable.csv"

    # get header file
    header = read_in_tree_structure.read_first_line(file_name)

    if 'tag name' not in header:
        print('tag name, not found in file {}'.format(file_name))
        return

    loc_tagname = header.index('tag name')

    if 'cluster name' not in header:
        print('cluster name, not found in file {}'.format(file_name))
        return

    loc_cluster = header.index('cluster name')

    # get most common schema
    max_count = 8000000  # limit read in while testing
    top_schema = find_equip_and_tree.read_in_schema(file_name, loc_tagname, max_count)
    print('schema = {}'.format(top_schema))

    # get position of equipment type
    mode = 1  # 1 character area designation
    percent_filter = 92
    data_base = find_equip_and_tree.find_equip_type_position_and_import_data(
                    file_name, loc_tagname, loc_cluster, max_count, top_schema, mode, percent_filter)

    equip_level_tree = data_base[0][0]
    if equip_level_tree >= 0:
        print('-equipment is located at position {} in the schema'.format(equip_level_tree + 1))

    # is 2 character mode needed
    first_level_tree = data_base[0][1]
    if first_level_tree < 0:  # try 2ch mode
        print('-try find equip position and first area in 2ch numeric mode')
        mode = 2  # chr area designation
        percent_filter = 98
        data_base = find_equip_and_tree.find_equip_type_position_and_import_data(
                        file_name, loc_tagname, loc_cluster, max_count, top_schema, mode, percent_filter)

    # get area hierarchy
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
            # get area hierarchy again
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
    is_item_found = 0
    if first_level_tree >= 0:
        data_base, is_item_found = find_equip_and_tree.find_item(file_name, loc_tagname, loc_cluster,
                                                                 max_count, top_schema, data_base, mode)

        equip_level_tree = data_base[0][0]
        first_level_tree = data_base[0][1]
        second_level_tree = data_base[0][2]
        third_level_tree = data_base[0][3]
        fourth_level_tree = data_base[0][4]
        last_digit = data_base[0][5]
        if last_digit < fourth_level_tree + mode - 1 \
                or last_digit < third_level_tree + mode - 1 \
                or last_digit < second_level_tree + mode - 1 \
                or last_digit < first_level_tree + mode - 1 \
                or last_digit < equip_level_tree:
            print('Warning equip number part start is before area digit')

    if is_item_found:
        data_base = find_equip_and_tree.find_equipment(top_schema, data_base)
        equip_num_start = data_base[0][6]
        equip_num_end = data_base[0][7]
        print('- equip digit found from position {} to position {}'.format(equip_num_start + 1, equip_num_end + 1))

        last_digit = data_base[0][5]
        print('- item found from position {}'.format(last_digit + 1))

        # print final tree
        print('-first level is at schema position {}'.format(first_level_tree + 1))  # convert to 1 base
        if second_level_tree >= 0:
            print('-second level is at schema position {}'.format(second_level_tree + 1))  # convert to 1 base
        if third_level_tree >= 0:
            print('-third level is at schema position {}'.format(third_level_tree + 1))  # convert to 1 base
        if fourth_level_tree >= 0:
            print('-fourth level is at schema position {}'.format(fourth_level_tree + 1))  # convert to 1 base

        # generate map schema
        matrix0 = data_base[0]
        map_schema = encode_decode_map_schema.encode_mapping_schema(matrix0, mode, top_schema)

        # generate config file
        print('Creating mapping file at path given')
        print('-map schema {}'.format(map_schema))

        # - create an equipment tree based on found schema so we can create a file for mapping
        data_base = read_in_tree_structure.get_equipment_tree(file_name, loc_tagname, loc_cluster,
                                                              max_count, map_schema, data_base, mode)

        area_list = sorted(data_base[1][0])  # cluster: Area.Area
        equip_type_list = sorted(data_base[3]) # equipment types
        item_type_list = sorted(data_base[2]) # item types
        write_read_config_file.write_config(config_file, map_schema, area_list, equip_type_list, item_type_list)
        print('Mapping file writen for schema found')
    else:
        write_read_config_file.write_config(config_file, 'AEXNNxI', [], [], [])
        print('Error Schema not found. Default mapping file writen. Please manually edit')


def main(file_path=''):
    if file_path == '':
        # file_path = 'D:\\Import\\example'  # set a default file name
        file_path = 'D:\\Import\\site1'  # set a default file name
        # file_path = 'C:\\ProgramData\\Schneider Electric\\Citect SCADA 2018\\User\\examplename\\'

        print('Argument not entered. using default {}'.format(file_path))

    file_path = file_path.rstrip('\\')

    # look for variables.dbf
    dbf_file = file_path + '\\variable.dbf'
    dbf_file_exists = os.path.isfile(dbf_file)
    if dbf_file_exists:
        map_dbf_to_csv(file_path)  # todo move this to next if statement.

    config_file = file_path + '\\mapping.ini'
    config_file_exists = os.path.isfile(config_file)
    # config_file_exists = False  # for testing. force re-generation of config file
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
