import read_in_tree_structure


def write_config(config_file, map_schema, equipment_list):
    matrix0, mode, schema = read_in_tree_structure.decode_mapping_schema(map_schema)
    equip_level_tree = matrix0[0]
    first_level_tree = matrix0[1]
    second_level_tree = matrix0[2]
    third_level_tree = matrix0[3]
    fourth_level_tree = matrix0[4]
    last_digit = matrix0[5]
    with open(config_file, mode='wt', encoding='utf-8') as f:
        f.write('[Schema]\n')
        f.write('Schema = {}\n'.format(map_schema))

        f.write('[Area Mapping]\n')
        if mode == 2:
            mapping = "Aa"
            if not second_level_tree == -1:
                mapping = mapping + ".Bb"
            if not third_level_tree == -1:
                mapping = mapping + ".Cc"
            if not fourth_level_tree == -1:
                mapping = mapping + ".Dd"
        else:
            mapping = "A"
            if not second_level_tree == -1:
                mapping = mapping + ".B"
            if not third_level_tree == -1:
                mapping = mapping + ".C"
            if not fourth_level_tree == -1:
                mapping = mapping + ".D"

        f.write('format = {}\n'.format(mapping))

        f.write('[Equipment Name Mapping]\n')
        for equip in equipment_list:
            cluster = equip[0:equip.find(":")]
            equipment = equip[equip.find(":") + 1:]
            f.write('Cluster({}) Area({}) Name = {}\n'.format(cluster, equipment, equipment))