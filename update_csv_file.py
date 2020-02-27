import encode_decode_map_schema
import read_csv_file


def add_string(g_tag, level_tree, mode):
    string = g_tag[level_tree]
    if mode == 2:
        string += g_tag[level_tree + 1]
    return string


def update_csv(map_schema, area_map, equipment_map_dict, loc_equip, loc_item, loc_tagname,
               loc_cluster, loc_iodev, file_name, equip_list):
    scratch_file = file_name.replace('.csv', '-working.csv')
    with open(scratch_file, mode='wt', encoding='utf-8') as sf:
        with open(file_name, mode='rt', encoding='utf-8') as rf:
            read_in_record_count = 0
            for read_line in rf:
                tag = read_csv_file.read_in_data(loc_tagname, read_line.strip()).strip('"')
                cluster = read_csv_file.read_in_data(loc_cluster, read_line.strip()).strip('"')
                item = read_csv_file.read_in_data(loc_item, read_line.strip()).strip('"')
                equipment = read_csv_file.read_in_data(loc_equip, read_line.strip()).strip('"')
                iodev = read_csv_file.read_in_data(loc_iodev, read_line.strip()).strip('"')

                mod_line = read_line
                read_in_record_count += 1
                if read_in_record_count > 1 and equipment == '':
                    current_schema, g_tag = read_csv_file.get_schema(tag)

                    matrix0, mode, generalised_schema = encode_decode_map_schema.decode_mapping_schema(map_schema)
                    generalised_current_schema = encode_decode_map_schema.generalise_schema(matrix0, mode, current_schema)
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

                        # look up equip dictonary mapping
                        equip_key = cluster + ':' + equip
                        if equip_key in equipment_map_dict:
                            equip = equipment_map_dict[equip_key]

                        # construct item
                        item = ''
                        if equip_level_tree >= 0:
                            item += g_tag[equip_level_tree]

                        for index in range(len(current_schema)):
                            if index >= last_digit:
                                item += g_tag[index]

                        # insert equip and item into mod_line
                        record_list = mod_line.rsplit(',')
                        record_list[loc_item] = '\"' + item + '\"'
                        record_list[loc_equip] = '\"' + equip + '\"'
                        mod_line = ','.join(record_list)

                # record all equipment
                cluster = read_csv_file.read_in_data(loc_cluster, mod_line.strip()).strip('"')
                equipment = read_csv_file.read_in_data(loc_equip, mod_line.strip()).strip('"')

                equip_key = cluster + ':' + equipment
                if not equipment == '' and read_in_record_count > 1:
                    if equip_key not in equip_list:
                        equip_list[equip_key] = iodev
                    elif len(iodev) > 0:
                        equip_list[equip_key] = iodev

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
                    cluster = read_csv_file.read_in_data(loc_cluster, read_line.strip()).strip('"')
                    equipment = read_csv_file.read_in_data(loc_equip, read_line.strip()).strip('"')
                    equip_key = cluster + ':' + equipment
                    if equip_key in equip_list:
                        # remove equipment entry
                        del equip_list[equip_key]

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

    print('final equip list length = {}'.format(len(equip_list)))
