import encode_decode_map_schema


def read_config_file(config_file):
    equipment_map_dict = dict()
    with open(config_file, mode='rt', encoding='utf-8') as f:
        for read_line in f:
            line = read_line.strip()
            if line == '[Schema]':
                map_schema = f.readline().strip()
                map_schema = map_schema[map_schema.find('=') + 1:].strip()

            if line == '[Area Mapping]':
                area_map = f.readline().strip()
                area_map = area_map[area_map.find('=') + 1:].strip()

            if line == '[Equipment Name Mapping]':
                for read_line in f:
                    equip_list = read_line.strip().rsplit('(')
                    cluster = equip_list[1][0:equip_list[1].find(')')]
                    area_numbers = equip_list[2][0:equip_list[2].find(')')]
                    area_name = equip_list[2][equip_list[2].find('=') + 1:].strip()
                    equipment_map_dict[cluster + ':' + area_numbers] = area_name

    return map_schema, area_map, equipment_map_dict


def write_config(config_file, map_schema, equipment_list):
    matrix0, mode, schema = encode_decode_map_schema.decode_mapping_schema(map_schema)
    second_level_tree = matrix0[2]
    third_level_tree = matrix0[3]
    fourth_level_tree = matrix0[4]
    with open(config_file, mode='wt', encoding='utf-8') as f:
        f.write('[Schema]\n')
        f.write('Schema = {}\n'.format(map_schema))

        f.write('[Area Mapping]\n')
        if mode == 2:
            mapping = "Aa"
            if not second_level_tree == -1:
                mapping += ".Bb"
            if not third_level_tree == -1:
                mapping += ".Cc"
            if not fourth_level_tree == -1:
                mapping += ".Dd"
        else:
            mapping = "A"
            if not second_level_tree == -1:
                mapping += ".B"
            if not third_level_tree == -1:
                mapping += ".C"
            if not fourth_level_tree == -1:
                mapping += ".D"

        f.write('format = {}\n'.format(mapping))

        f.write('[Equipment Name Mapping]\n')
        for equip in equipment_list:
            cluster = equip[0:equip.find(":")]
            equipment = equip[equip.find(":") + 1:]
            f.write('Cluster({}) Area({}) Name = {}\n'.format(cluster, equipment, equipment))