def get_schema(tag):
    schema = ''
    schema_char_type = ''
    g_tag = []

    for char in tag:
        if char.isalpha():
            if not schema_char_type == "W":
                schema_char_type = "W"
                schema += schema_char_type
                g_tag.append(char)
            else:
                g_tag[len(g_tag) - 1] += char

        if char.isnumeric():
            schema_char_type = "N"
            schema += schema_char_type
            g_tag.append(char)

        if not char.isalnum():
            schema_char_type = char  # record delineator schema_char_type
            schema += schema_char_type
            g_tag.append(char)

    return schema, g_tag


def read_in_data(data_loc, line_str):
    record_list = line_str.rsplit(',')
    return record_list[data_loc]


def is_tag_part_used(tag_part, schema, matrix0, mode):
    equip_level_tree = matrix0[0]
    first_level_tree = matrix0[1]
    second_level_tree = matrix0[2]
    third_level_tree = matrix0[3]
    fourth_level_tree = matrix0[4]

    tag_part_is_used = 0
    if tag_part == equip_level_tree \
            or tag_part == first_level_tree \
            or tag_part == first_level_tree + 1 and mode == 2 \
            or tag_part == second_level_tree \
            or tag_part == second_level_tree + 1 and mode == 2 \
            or tag_part == third_level_tree \
            or tag_part == third_level_tree + 1 and mode == 2 \
            or tag_part == fourth_level_tree \
            or tag_part == fourth_level_tree + 1 and mode == 2 \
            or not schema[tag_part:tag_part + 1].isalpha():
        tag_part_is_used = 1

    return tag_part_is_used


def add_equip_part(g_tag, level_tree, mode):
    eq_part = g_tag[level_tree]
    if mode == 2:
        eq_part += g_tag[level_tree + 1]

    return eq_part
