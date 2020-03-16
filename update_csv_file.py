import encode_decode_map_schema
import tag_utils


def update_csv(map_schema, area_map, loc_equip, loc_item, loc_tagname, loc_cluster, loc_iodev, loc_project_name,
               file_name, new_equip_list, equipment_map_dict, equipment_type_map_dict, item_type_map_dict,
               area_prefix_map_dict):
    scratch_file = file_name.replace('.csv', '-working.csv')
    with open(scratch_file, mode='wt', encoding='utf-8') as sf:
        existing_cluster_equip_item_list = list()
        with open(file_name, mode='rt', encoding='utf-8') as rf:
            read_in_record_count = 0
            for read_line in rf:
                read_in_record_count += 1
                if read_in_record_count > 1:
                    existing_csv_equipment = tag_utils.read_in_data(loc_equip, read_line.strip())
                    if not existing_csv_equipment == '':
                        exiting_csv_tag = tag_utils.read_in_data(loc_tagname, read_line.strip())
                        existing_csv_cluster = tag_utils.read_in_data(loc_cluster, read_line.strip())
                        existing_csv_item = tag_utils.read_in_data(loc_item, read_line.strip())
                        if existing_csv_item == '':  # citect will use tag if no item is defined so record tag for item
                            existing_csv_item = exiting_csv_tag

                        equip_key = existing_csv_cluster + ':' + existing_csv_equipment
                        if equip_key.lower() not in existing_cluster_equip_item_list:
                            existing_cluster_equip_item_list.append(equip_key.lower())

        with open(file_name, mode='rt', encoding='utf-8') as rf:
            read_in_record_count = 0
            for read_line in rf:
                mod_line = read_line
                read_in_record_count += 1
                if read_in_record_count > 1:
                    exiting_csv_tag = tag_utils.read_in_data(loc_tagname, read_line.strip())
                    existing_csv_equipment = tag_utils.read_in_data(loc_equip, read_line.strip())

                    matrix0, mode, generalised_schema = encode_decode_map_schema.decode_mapping_schema(map_schema)

                    current_schema, g_tag = tag_utils.get_schema(exiting_csv_tag)
                    generalised_current_schema = encode_decode_map_schema.generalise_schema(matrix0, mode,
                                                                                            current_schema)
                    if generalised_current_schema.find(generalised_schema) == 0 and existing_csv_equipment == '':
                        existing_csv_cluster = tag_utils.read_in_data(loc_cluster, read_line.strip())
                        existing_csv_iodev = tag_utils.read_in_data(loc_iodev, read_line.strip())
                        exiting_csv_project_name = tag_utils.read_in_data(loc_project_name, read_line.strip())

                        # construct equipment
                        equip_level_tree = matrix0[0]
                        first_level_tree = matrix0[1]
                        second_level_tree = matrix0[2]
                        third_level_tree = matrix0[3]
                        fourth_level_tree = matrix0[4]
                        last_digit = matrix0[5]
                        equip_num_start = matrix0[6]
                        equip_num_end = matrix0[7]

                        prefix_area_key = ''
                        new_equip = '.'
                        area_key = ''
                        for chars in area_map.rsplit('.'):
                            if chars.find('Prefix') == 1:
                                # get prefix + Area
                                char = chars[len('xPrefix'):]
                                prefix = chars[0:len('xPrefix')]
                                if char == 'A' and first_level_tree >= 0:
                                    area_key += tag_utils.add_equip_part(g_tag, first_level_tree, mode)
                                    prefix_area_key += area_prefix_map_dict[prefix] + \
                                                 tag_utils.add_equip_part(g_tag, first_level_tree, mode)
                                elif char == 'B' and second_level_tree >= 0:
                                    area_key += '.' + tag_utils.add_equip_part(g_tag, second_level_tree, mode)
                                    prefix_area_key += '.' + area_prefix_map_dict[prefix] + \
                                                 tag_utils.add_equip_part(g_tag, second_level_tree, mode)
                                elif char == 'C' and third_level_tree >= 0:
                                    area_key += '.' + tag_utils.add_equip_part(g_tag, third_level_tree, mode)
                                    prefix_area_key += '.' + area_prefix_map_dict[prefix] + \
                                                 tag_utils.add_equip_part(g_tag, third_level_tree, mode)
                                elif char == 'D' and fourth_level_tree >= 0:
                                    area_key += '.' + tag_utils.add_equip_part(g_tag, fourth_level_tree, mode)
                                    prefix_area_key += '.' + area_prefix_map_dict[prefix] + \
                                                 tag_utils.add_equip_part(g_tag, fourth_level_tree, mode)
                            else:
                                # add equip type + equip numbers
                                for char in chars:
                                    if char == 'E':
                                        new_equip += equipment_type_map_dict[g_tag[equip_level_tree]]
                                    if char == 'X':
                                        for index in range(len(current_schema)):
                                            if index >= equip_num_start and index <= equip_num_end:
                                                new_equip += g_tag[index]

                        # construct item
                        item = ''
                        for index in range(len(current_schema)):
                            if index >= last_digit:
                                item += g_tag[index]

                        if item in item_type_map_dict:
                            new_item = item_type_map_dict[item]
                        else:
                            new_item = item

                        # record all new equipment + iodevice and project name
                        new_area_key = existing_csv_cluster + ':' + area_key
                        if new_area_key in equipment_map_dict:
                            # if mapped area is not the same as default then add prefix
                            if not new_area_key == existing_csv_cluster + ':' + equipment_map_dict[new_area_key]:
                                prefix_area_key = equipment_map_dict[new_area_key]

                        prefix_area_key += new_equip

                        cluster_area_key = existing_csv_cluster + ':' + prefix_area_key

                        # check if area parts and equip part is valid
                        is_key_valid = 0
                        for area in cluster_area_key[cluster_area_key.find(':')+1:].rsplit('.'):
                            if len(area) == 0:
                                is_key_valid = 0
                                break
                            else:
                                is_key_valid = 1

                        if is_key_valid:
                            # add to new equipment to list if not used anywhere
                            is_key_exists = 0
                            if cluster_area_key in new_equip_list:
                                is_key_exists = 1

                            if not is_key_exists and not cluster_area_key.lower() in existing_cluster_equip_item_list:
                                new_equip_list[cluster_area_key] = [existing_csv_iodev, exiting_csv_project_name]

                            # insert equip and item into mod_line if equipment generated is valid and cell empty
                            record_list = mod_line.rsplit(',"')
                            if record_list[loc_equip] == '""':
                                for index in range(len(record_list)):
                                    record_list[index] = '\"' + record_list[index]  # add leading "

                                record_list[loc_item] = '\"' + new_item + '\"'
                                record_list[loc_equip] = '\"' + prefix_area_key + '\"'

                                mod_line = ','.join(record_list)

                sf.write(mod_line)

    return new_equip_list


def update_equipment_csv(loc_equip, loc_cluster, loc_iodev, loc_project_name, file_name, new_equip_list):
    scratch_file = file_name.replace('.csv', '-working.csv')
    with open(scratch_file, mode='wt', encoding='utf-8') as sf:
        # read existing equipment and delete from new equipment list if match
        with open(file_name, mode='rt', encoding='utf-8') as rf:
            read_in_record_count = 0
            for read_line in rf:
                read_in_record_count += 1
                sf.write(read_line)  # copy existing lines
                if read_in_record_count > 1:
                    cluster = tag_utils.read_in_data(loc_cluster, read_line.strip()).strip('"')
                    equipment = tag_utils.read_in_data(loc_equip, read_line.strip()).strip('"')
                    equip_key = cluster + ':' + equipment

                    is_duplicate = 0
                    for key in new_equip_list:
                        if equip_key.lower() == key.lower():
                            is_duplicate = 1

                    if is_duplicate:
                        del new_equip_list[key]  # remove equipment entry as it already exists
                else:
                    header = read_line

        # clear line so it can be used as a template
        new_list = header.rsplit(',')
        for item in range(len(new_list)):
            new_list[item] = '""'

        for equipment in new_equip_list:
            cluster = equipment[0:equipment.find(':')]
            equip = equipment[equipment.find(':') + 1:]
            new_list[loc_cluster] = '\"' + cluster + '\"'
            new_list[loc_equip] = '\"' + equip + '\"'

            iodev = new_equip_list[equipment][0]
            project_name = new_equip_list[equipment][1]
            if len(iodev) > 0:
                new_list[loc_iodev] = '\"' + iodev + '\"'

            if len(project_name) > 0:
                new_list[loc_project_name] = '\"' + project_name + '\"'

            mod_line = '\n' + ','.join(new_list)

            sf.write(mod_line)  # write new line
            read_in_record_count += 1
