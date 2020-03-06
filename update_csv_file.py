import encode_decode_map_schema
import tag_utils


def update_csv(map_schema, area_map, loc_equip, loc_item, loc_tagname,
               loc_cluster, loc_iodev, loc_project_name, file_name, new_equip_list, equipment_map_dict):
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
                        if existing_csv_item == '':
                            existing_csv_item = exiting_csv_tag  # citect will use tag if no item is defined so record tag for item

                        equip_key = existing_csv_cluster + ':' + existing_csv_equipment + ":" + existing_csv_item
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

                        new_equip = ''
                        for char in area_map:
                            if char == 'A' and first_level_tree >= 0:
                                new_equip += tag_utils.add_equip_part(g_tag, first_level_tree, mode)
                            elif char == 'B' and second_level_tree >= 0:
                                new_equip += tag_utils.add_equip_part(g_tag, second_level_tree, mode)
                            elif char == 'C' and third_level_tree >= 0:
                                new_equip += tag_utils.add_equip_part(g_tag, third_level_tree, mode)
                            elif char == 'D' and fourth_level_tree >= 0:
                                new_equip += tag_utils.add_equip_part(g_tag, fourth_level_tree, mode)
                            elif char == '.':
                                new_equip += '.'

                        # construct equip_type + item
                        new_item = ''
                        if equip_level_tree >= 0:
                            new_item += g_tag[equip_level_tree]

                        for index in range(len(current_schema)):
                            if index >= last_digit:
                                new_item += g_tag[index]

                        # record all new equipment + iodevice and project name
                        new_equip_key = existing_csv_cluster + ':' + new_equip
                        if new_equip_key not in equipment_map_dict:
                            maped_equip_key = new_equip_key  # should only get invoked if key in  mapping.ini
                        else:
                            maped_equip_key = existing_csv_cluster + ':' + equipment_map_dict[new_equip_key]

                        # add to new equipment to list if not used anywere
                        key_exists = 0
                        for key in new_equip_list:
                            if maped_equip_key.lower() == key.lower():
                                key_exists = 1
                                break

                        if maped_equip_key not in new_equip_list and key_exists == 0:
                            new_equip_list[maped_equip_key] = [existing_csv_iodev, exiting_csv_project_name]

                        # check if equip.item is already used
                        equip_key = maped_equip_key + ":" + new_item
                        if equip_key.lower() in existing_cluster_equip_item_list:
                            new_item = exiting_csv_tag  # fallback to tag to prevent duplicate equip.item ref

                        # insert equip and item into mod_line
                        record_list = mod_line.rsplit(',"')
                        for index in range(len(record_list)):
                            record_list[index] = '\"' + record_list[index] # add leading "

                        record_list[loc_item] = '\"' + new_item + '\"'
                        record_list[loc_equip] = '\"' + new_equip + '\"'

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
