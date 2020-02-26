import read_csv_file

def decode_mapping_schema(map_schema):
    matrix0 = [-1,-1,-1,-1,-1,-1]
    equip_level_tree = matrix0[0]
    first_level_tree = matrix0[1]
    second_level_tree = matrix0[2]
    third_level_tree = matrix0[3]
    fourth_level_tree = matrix0[4]
    last_digit = matrix0[5]

    schema = map_schema

    mode = 1
    for index in range(len(map_schema)):
        char = map_schema[index:index + 1]
        if char == 'E':
            equip_level_tree = index
        elif char == 'I':
            last_digit = index
        elif char == 'A':
            first_level_tree = index
        elif char == 'B':
            second_level_tree = index
        elif char == 'C':
            third_level_tree = index
        elif char == 'D':
            fourth_level_tree = index
        elif char == 'a' or char == 'b' or char == 'c' or char == 'd':
            mode = 2

        if char == 'a' or char == 'b' or char == 'c' or char == 'd':
            schema = schema[0:index] + "N" + schema[index + 1:]
        elif char == 'A' or char == 'B' or char == 'C' or char == 'D':
            schema = schema[0:index] + "N" + schema[index + 1:]
        elif char == 'E':
            schema = schema[0:index] + "W" + schema[index + 1:]
        elif char == 'I':
            schema = schema[0:index] + "W" + schema[index + 1:]
        elif char == 'i':
            schema = schema[0:index] + "N" + schema[index + 1:]

    matrix0[0] = equip_level_tree
    matrix0[1] = first_level_tree
    matrix0[2] = second_level_tree
    matrix0[3] = third_level_tree
    matrix0[4] = fourth_level_tree
    matrix0[5] = last_digit

    return matrix0, mode, schema


def get_equipment_tree(file_name, loc_tagname, loc_cluster, max_count, map_schema):
    matrix0, mode, schema = decode_mapping_schema(map_schema)
    data_base = []
    data_base.append(matrix0)
    data_base.append(dict())  # matrix - use for equipment tree
    data_base.append(list())  # equip_type_count_matrix - dummy place marker
    data_base.append(list())  # equip_matrix - dummy place marker

    search_digit = 2  # read in csv and make flat equip list with no equipment
    data_base,_ = read_csv_file.move_scenario_data_to_array(search_digit, file_name, loc_tagname, loc_cluster, max_count, schema,
                                data_base, mode)

    return data_base


def read_first_line(file_name):
    with open(file_name, mode='rt', encoding='utf-8') as f:
        return f.readline().strip().lower().rsplit(',')