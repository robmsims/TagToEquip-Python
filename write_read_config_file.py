import encode_decode_map_schema


def read_config_file(config_file):
    area_map_dict = dict()
    equipment_type_map_dict = dict()
    item_type_map_dict = dict()
    area_prefix_map_dict = dict()
    with open(config_file, mode='rt', encoding='utf-8') as f:
        for read_line in f:
            line = read_line.strip()
            if line == '[Schema]':
                map_schema = f.readline().strip()
                map_schema = map_schema[map_schema.find('=') + 1:].strip()

            if line == '[Area Mapping]':
                area_map = f.readline().strip()
                area_map = area_map[area_map.find('=') + 1:].strip()

            if line == '[Area Prefix Mapping]':
                for read_area_prefix in f:
                    if read_area_prefix == '\n':
                        break
                    equip_area = read_area_prefix[read_area_prefix.find('(') + 1:read_area_prefix.find(')')]
                    equip_area_prefix = read_area_prefix[read_area_prefix.find('=') + 1:].strip()
                    area_prefix_map_dict[equip_area] = equip_area_prefix

            if line == '[Area Name Mapping]':
                for read_area in f:
                    if read_area == '\n':
                        break
                    area_list = read_area.strip().rsplit('(')
                    cluster = area_list[1][0:area_list[1].find(')')]
                    area_numbers = area_list[2][0:area_list[2].find(')')]
                    area_name = area_list[2][area_list[2].find('=') + 1:].strip()
                    area_map_dict[cluster + ':' + area_numbers] = area_name

            if line == '[Equipment Type Mapping]':
                for read_equip_type in f:
                    if read_equip_type == '\n':
                        break
                    equip_type = read_equip_type[read_equip_type.find('(') + 1:read_equip_type.find(')')]
                    equip_type_friendly = read_equip_type[read_equip_type.find('=') + 1:].strip()
                    equipment_type_map_dict[equip_type] = equip_type_friendly

            if line == '[Item Type Mapping]':
                for read_item_type in f:
                    if read_item_type == '\n':
                        break
                    item_type = read_item_type[read_item_type.find('(') + 1:read_item_type.find(')')]
                    item_type_friendly = read_item_type[read_item_type.find('=') + 1:].strip()
                    item_type_map_dict[item_type] = item_type_friendly

    return map_schema, area_map, area_map_dict, equipment_type_map_dict, item_type_map_dict, area_prefix_map_dict


def write_config(config_file, map_schema, area_list, equip_type_list, item_type_list):
    matrix0, mode, schema = encode_decode_map_schema.decode_mapping_schema(map_schema)
    second_level_tree = matrix0[2]
    third_level_tree = matrix0[3]
    fourth_level_tree = matrix0[4]
    with open(config_file, mode='wt', encoding='utf-8') as f:
        f.write('[Schema]\n')
        f.write('Schema = {}\n'.format(map_schema))
        f.write('\n')

        f.write('[Area Prefix Mapping]\n')
        f.write('Area A prefix (aPrefix) = LVL1Area\n')
        f.write('Area B prefix (bPrefix) = LVL2Area\n')
        f.write('Area C prefix (cPrefix) = LVL3Area\n')
        f.write('Area D prefix (dPrefix) = LVL4Area\n')
        f.write('\n')

        f.write('[Area Mapping]\n')
        if mode == 2:
            mapping = "aPrefixAa"
            if not second_level_tree == -1:
                mapping += ".bPrefixBb"
            if not third_level_tree == -1:
                mapping += ".cPrefixCc"
            if not fourth_level_tree == -1:
                mapping += ".dPrefixDd"
        else:
            mapping = "aPrefixA"
            if not second_level_tree == -1:
                mapping += ".bPrefixB"
            if not third_level_tree == -1:
                mapping += ".cPrefixC"
            if not fourth_level_tree == -1:
                mapping += ".dPrefixD"
        mapping += '.EX'
        f.write('format = {}\n'.format(mapping))
        f.write('\n')

        f.write('[Area Name Mapping]\n')
        for area in area_list:
            cluster = area[0:area.find(":")]
            areas = area[area.find(":") + 1:]
            f.write('Cluster({}) Area({}) Name = {}\n'.format(cluster, areas, areas))
        f.write('\n')

        f.write('[Equipment Type Mapping]\n')
        for equip_type in equip_type_list:
            f.write('Equipment type friendly name for ({}) = {}\n'.format(equip_type, equip_type))
        f.write('\n')

        f.write('[Item Type Mapping]\n')
        for item_type in item_type_list:
            f.write('Item type friendly name for ({}) = {}\n'.format(item_type, item_type))