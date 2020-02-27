

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

        if char == 'a' or char == 'b' or char == 'c' or char == 'd':
            mode = 2
            schema = schema[0:index - 1] + "NN" + schema[index + 1:]
        elif char == 'A' or char == 'B' or char == 'C' or char == 'D':
            schema = schema[0:index] + "*" + schema[index + 1:]
        elif char == 'I':
            schema = schema[0:index] + "*" + schema[index + 1:]
        elif char == 'E':
            schema = schema[0:index] + "W" + schema[index + 1:]

    matrix0[0] = equip_level_tree
    matrix0[1] = first_level_tree
    matrix0[2] = second_level_tree
    matrix0[3] = third_level_tree
    matrix0[4] = fourth_level_tree
    matrix0[5] = last_digit

    return matrix0, mode, schema


def encode_mapping_schema(matrix0, mode, top_schema):
    equip_level_tree = matrix0[0]
    first_level_tree = matrix0[1]
    second_level_tree = matrix0[2]
    third_level_tree = matrix0[3]
    fourth_level_tree = matrix0[4]
    last_digit = matrix0[5]

    map_schema = top_schema

    # find end of mapping
    end_schema = 0
    if first_level_tree >= 0:
        map_schema = map_schema[0:first_level_tree] + "A" + map_schema[first_level_tree + 1:]
        end_schema = first_level_tree
    if first_level_tree >= 0 and mode == 2:
        map_schema = map_schema[0:first_level_tree + 1] + "a" + map_schema[first_level_tree + 2:]
        end_schema = first_level_tree + 1

    if second_level_tree >= 0:
        map_schema = map_schema[0:second_level_tree] + "B" + map_schema[second_level_tree + 1:]
        end_schema = second_level_tree
    if second_level_tree >= 0 and mode == 2:
        map_schema = map_schema[0:second_level_tree + 1] + "b" + map_schema[second_level_tree + 2:]
        end_schema = second_level_tree + 1

    if third_level_tree >= 0:
        map_schema = map_schema[0:third_level_tree] + "C" + map_schema[third_level_tree + 1:]
        end_schema = third_level_tree
    if third_level_tree >= 0 and mode == 2:
        map_schema = map_schema[0:third_level_tree + 1] + "c" + map_schema[third_level_tree + 2:]
        end_schema = third_level_tree + 1

    if fourth_level_tree >= 0:
        map_schema = map_schema[0:fourth_level_tree] + "D" + map_schema[fourth_level_tree + 1:]
        end_schema = fourth_level_tree
    if fourth_level_tree >= 0 and mode == 2:
        map_schema = map_schema[0:fourth_level_tree + 1] + "d" + map_schema[fourth_level_tree + 2:]
        end_schema = fourth_level_tree + 1

    map_schema = map_schema[0:equip_level_tree] + "E" + map_schema[equip_level_tree + 1:]
    if equip_level_tree > end_schema:
        end_schema = equip_level_tree

    # do next bit only if Item has been found
    if not last_digit == -1:
        char = top_schema[last_digit:last_digit + 1]
        if last_digit > end_schema:
            end_schema = last_digit
            map_schema = map_schema[0:last_digit] + "I"
        else:
            print('Warning item part start is before area digit')
            map_schema = map_schema[0:last_digit] + "I" + map_schema[last_digit + 1:]

        map_schema = map_schema[0:end_schema + 1]

    # replace 'W' or 'N' with '*'
    for index in range(len(map_schema)):
        char = map_schema[index:index + 1]
        if char == 'N' or char == 'W':
            map_schema = map_schema[0:index] + '*' + map_schema[index + 1:]

    return map_schema


def generalise_schema(data_base, mode, schema):
    map_schema = encode_mapping_schema(data_base, mode, schema)
    matrix0, mode, generalised_schema = decode_mapping_schema(map_schema)
    return generalised_schema
