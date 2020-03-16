def decode_mapping_schema(map_schema):
    matrix0 = [-1, -1, -1, -1, -1, -1, -1, -1]
    equip_level_tree = matrix0[0]
    first_level_tree = matrix0[1]
    second_level_tree = matrix0[2]
    third_level_tree = matrix0[3]
    fourth_level_tree = matrix0[4]
    last_digit = matrix0[5]
    equip_num_start = matrix0[6]
    equip_num_end = matrix0[7]

    schema = map_schema

    mode = 1
    for index in range(len(map_schema)):
        char = map_schema[index:index + 1]
        if char == 'E':
            equip_level_tree = index
        elif char == 'X':
            equip_num_start = index
        elif char == 'x':
            equip_num_end = index
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

        if char == 'a' or char == 'b' or char == 'c' or char == 'd':
            mode = 2
            if schema[index - 1:index] == '*':
                schema = schema[0:index - 1] + "NN" + schema[index + 1:]
        elif char == 'A' or char == 'B' or char == 'C' or char == 'D':
            schema = schema[0:index] + "*" + schema[index + 1:]
        elif char == 'I':
            schema = schema[0:index] + "*" + schema[index + 1:]
        elif char == 'E':
            schema = schema[0:index] + "W" + schema[index + 1:]
        elif char == 'X':
            schema = schema[0:index] + "*" + schema[index + 1:]
        elif char == 'x':
            schema = schema[0:index] + "*" + schema[index + 1:]

    matrix0[0] = equip_level_tree
    matrix0[1] = first_level_tree
    matrix0[2] = second_level_tree
    matrix0[3] = third_level_tree
    matrix0[4] = fourth_level_tree
    matrix0[5] = last_digit
    matrix0[6] = equip_num_start
    matrix0[7] = equip_num_end

    return matrix0, mode, schema


def insert_into_map_schema(map_schema, end_schema, level_tree, mode, string):
    string = string[0:mode]

    if len(map_schema) >= level_tree + (mode - 1):  # don't write into a position that doesn't exist
        if map_schema[level_tree:level_tree + 1].isalnum():
            if mode == 1 or (mode == 2 and not map_schema[level_tree:level_tree + 1].isalnum()):
                map_schema = map_schema[0:level_tree] + string + map_schema[level_tree + mode:]
                if level_tree > end_schema:
                    end_schema = level_tree + (mode - 1)  # cater for 2ch mode

    return map_schema, end_schema


def encode_mapping_schema(matrix0, mode, top_schema):
    equip_level_tree = matrix0[0]
    first_level_tree = matrix0[1]
    second_level_tree = matrix0[2]
    third_level_tree = matrix0[3]
    fourth_level_tree = matrix0[4]
    last_digit = matrix0[5]
    equip_num_start = matrix0[6]
    equip_num_end = matrix0[7]

    map_schema = top_schema

    # find end of mapping
    end_schema = 0
    if first_level_tree >= 0:
        map_schema, end_schema = insert_into_map_schema(map_schema, end_schema, first_level_tree, mode, 'Aa')

    if second_level_tree >= 0:
        map_schema, end_schema = insert_into_map_schema(map_schema, end_schema, second_level_tree, mode, 'Ba')

    if third_level_tree >= 0:
        map_schema, end_schema = insert_into_map_schema(map_schema, end_schema, third_level_tree, mode, 'Cc')

    if fourth_level_tree >= 0:
        map_schema, end_schema = insert_into_map_schema(map_schema, end_schema, fourth_level_tree, mode, 'Dd')

    if equip_level_tree >= 0:
        map_schema, end_schema = insert_into_map_schema(map_schema, end_schema, equip_level_tree, 1, 'E')

    if equip_num_start >= 0 and equip_num_end >= 0:
        map_schema, end_schema = insert_into_map_schema(map_schema, end_schema, equip_num_start, 1, 'X')
        map_schema, end_schema = insert_into_map_schema(map_schema, end_schema, equip_num_end, 1, 'x')

    if last_digit >= 0:
        map_schema, end_schema = insert_into_map_schema(map_schema, end_schema, last_digit, 1, 'I')
        map_schema = map_schema[0:end_schema + 1]  # only truncate when looking for item

    return map_schema


def generalise_schema(data_base, mode, schema):
    map_schema = encode_mapping_schema(data_base, mode, schema)
    matrix0, mode, generalised_schema = decode_mapping_schema(map_schema)
    return generalised_schema
