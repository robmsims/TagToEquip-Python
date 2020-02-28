import encode_decode_map_schema
import tag_utils


def add_string(g_tag, level_tree, mode):
    string = g_tag[level_tree]
    if mode == 2:
        string += g_tag[level_tree + 1]
    return string


def update_csv(map_schema, area_map, loc_equip, loc_item, loc_tagname,
               loc_cluster, loc_iodev, file_name, equip_list):
    scratch_file = file_name.replace('.csv', '-working.csv')
    with open(scratch_file, mode='wt', encoding='utf-8') as sf:
        existing_cluster_equip_item_list = list()
        with open(file_name, mode='rt', encoding='utf-8') as rf:
            read_in_record_count = 0
            for read_line in rf:
                tag = tag_utils.read_in_data(loc_tagname, read_line.strip()).strip('"')
                cluster = tag_utils.read_in_data(loc_cluster, read_line.strip()).strip('"')
                item = tag_utils.read_in_data(loc_item, read_line.strip()).strip('"')
                equipment = tag_utils.read_in_data(loc_equip, read_line.strip()).strip('"')

                read_in_record_count += 1
                if read_in_record_count > 1 and not equipment == '':
                    if item == '':
                        item = tag  # citect will use tag if no item is defined so record tag for item

                    equip_key = cluster + ':' + equipment + ":" + item
                    if equip_key not in existing_cluster_equip_item_list:
                        existing_cluster_equip_item_list.append(equip_key)

        with open(file_name, mode='rt', encoding='utf-8') as rf:
            read_in_record_count = 0
            for read_line in rf:
                tag = tag_utils.read_in_data(loc_tagname, read_line.strip()).strip('"')
                cluster = tag_utils.read_in_data(loc_cluster, read_line.strip()).strip('"')
                equipment = tag_utils.read_in_data(loc_equip, read_line.strip()).strip('"')
                iodev = tag_utils.read_in_data(loc_iodev, read_line.strip()).strip('"')

                mod_line = read_line
                read_in_record_count += 1
                if read_in_record_count > 1 and equipment == '':
                    current_schema, g_tag = tag_utils.get_schema(tag)

                    matrix0, mode, generalised_schema = encode_decode_map_schema.decode_mapping_schema(map_schema)
                    generalised_current_schema = encode_decode_map_schema.generalise_schema(matrix0, mode,
                                                                                            current_schema)
                    if generalised_current_schema.find(generalised_schema) == 0:
                        # construct equipment
                        equip_level_tree = matrix0[0]
                        first_level_tree = matrix0[1]
                        second_level_tree = matrix0[2]
                        third_level_tree = matrix0[3]
                        fourth_level_tree = matrix0[4]
                        last_digit = matrix0[5]

                        equip = ''
                        for char in area_map:
                            if char == 'A' and first_level_tree >= 0:
                                equip += add_string(g_tag, first_level_tree, mode)
                            elif char == 'B' and second_level_tree >= 0:
                                equip += add_string(g_tag, second_level_tree, mode)
                            elif char == 'C' and third_level_tree >= 0:
                                equip += add_string(g_tag, third_level_tree, mode)
                            elif char == 'D' and fourth_level_tree >= 0:
                                equip += add_string(g_tag, fourth_level_tree, mode)
                            elif char == '.':
                                equip += '.'

                        # construct equip_type + item
                        item = ''
                        if equip_level_tree >= 0:
                            item += g_tag[equip_level_tree]

                        for index in range(len(current_schema)):
                            if index >= last_digit:
                                item += g_tag[index]

                        # record all new equipment + iodevice if missing
                        equip_key = cluster + ':' + equip
                        if equip_key not in equip_list:
                            equip_list[equip_key] = iodev
                        elif len(iodev) > 0:  # i/o device only in variables.csv
                            equip_list[equip_key] = iodev

                        # check if equip.item is already used
                        equip_key = cluster + ':' + equipment + ":" + item
                        if equip_key in existing_cluster_equip_item_list:
                            item = tag  # fallback to tag to prevent duplicate equip.item reference

                        # insert equip and item into mod_line
                        record_list = mod_line.rsplit(',')
                        record_list[loc_item] = '\"' + item + '\"'
                        record_list[loc_equip] = '\"' + equip + '\"'
                        mod_line = ','.join(record_list)

                sf.write(mod_line)

    return equip_list


def update_equipment_csv(loc_equip, loc_cluster, loc_iodev, file_name, equip_list):
    print('inital equip list length = {}'.format(len(equip_list)))
    scratch_file = file_name.replace('.csv', '-working.csv')
    with open(scratch_file, mode='wt', encoding='utf-8') as sf:
        with open(file_name, mode='rt', encoding='utf-8') as rf:
            read_in_record_count = 0
            for read_line in rf:
                read_in_record_count += 1
                sf.write(read_line)  # copy existing lines
                if read_in_record_count > 1:
                    cluster = tag_utils.read_in_data(loc_cluster, read_line.strip()).strip('"')
                    equipment = tag_utils.read_in_data(loc_equip, read_line.strip()).strip('"')
                    equip_key = cluster + ':' + equipment
                    if equip_key in equip_list:
                        # remove equipment entry
                        del equip_list[equip_key]

        print('final equip list length = {}'.format(len(equip_list)))

        # clear line so it can be used as a template
        record_list = read_line.rsplit(',')
        for item in range(len(record_list) - 1):
            record_list[item] = '""'

        for equipment in equip_list:
            new_list = record_list

            cluster = equipment[0:equipment.find(':')]
            equip = equipment[equipment.find(':') + 1:]
            new_list[loc_cluster] = '\"' + cluster + '\"'
            new_list[loc_equip] = '\"' + equip + '\"'

            iodev = equip_list[equipment]
            if len(iodev) > 0:
                new_list[loc_iodev] = '\"' + iodev + '\"'

            mod_line = ','.join(new_list)

            sf.write(mod_line)  # copy existing lines
