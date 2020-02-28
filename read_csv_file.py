import encode_decode_map_schema
import tag_utils


def store_equip(matrix_list, tree):
    if tree not in matrix_list:
        matrix_list.append(tree)


def send_equipment(g_tag, data_base, mode, cluster):
    # search_digit == 2
    first_level_tree = data_base[0][1]
    second_level_tree = data_base[0][2]
    third_level_tree = data_base[0][3]
    fourth_level_tree = data_base[0][4]

    matrix = data_base[1]

    index = 0
    if index not in matrix:
        matrix[index] = list()  # append an empty list for equip index position

    matrix_list = matrix[index]

    tree = cluster + ":" + g_tag[first_level_tree]
    if mode == 2:
        tree += g_tag[first_level_tree + 1]
    store_equip(matrix_list, tree)

    if second_level_tree >= 0:
        tree += '.' + g_tag[second_level_tree]
        if mode == 2:
            tree += g_tag[second_level_tree + 1]
        store_equip(matrix_list, tree)

    if third_level_tree >= 0:
        tree += '.' + g_tag[third_level_tree]
        if mode == 2:
            tree += g_tag[third_level_tree + 1]
        store_equip(matrix_list, tree)

    if fourth_level_tree >= 0:
        tree += '.' + g_tag[fourth_level_tree]
        if mode == 2:
            tree += g_tag[fourth_level_tree + 1]
        store_equip(matrix_list, tree)


def send_item_parts(g_tag, data_base, mode, schema, cluster):
    # search_digit == 1
    equip_level_tree = data_base[0][0]
    first_level_tree = data_base[0][1]
    second_level_tree = data_base[0][2]
    third_level_tree = data_base[0][3]
    fourth_level_tree = data_base[0][4]
    last_digit = data_base[0][5]

    matrix = data_base[1]

    equip_matrix = data_base[3]

    is_item_digits_found = 1
    eq_part = g_tag[equip_level_tree]
    if first_level_tree >= 0:
        eq_part += '.' + g_tag[first_level_tree]
        if mode == 2:
            eq_part += g_tag[first_level_tree + 1]

    if second_level_tree >= 0:
        eq_part += '.' + g_tag[second_level_tree]
        if mode == 2:
            eq_part += g_tag[second_level_tree + 1]

    if third_level_tree >= 0:
        eq_part += '.' + g_tag[third_level_tree]
        if mode == 2:
            eq_part += g_tag[third_level_tree + 1]

    if eq_part in equip_matrix:
        index = equip_matrix.index(eq_part)
        if index not in matrix:
            matrix[index] = list()  # append an empty list for equip index position

        is_item_digits_found = 0
        char = schema[last_digit:last_digit + 1]
        if not char.isalpha():
            return is_item_digits_found  # abort search for duplicates as we have a delineator

        list_matrix = matrix[index]  # get list containing tags for this equipment

        tag = cluster + "."
        for tag_part in range(0, len(schema)):  # only record on first part of item
            if tag_part == equip_level_tree \
                    or tag_part == first_level_tree \
                    or tag_part == first_level_tree + 1 and mode == 2 \
                    or tag_part == second_level_tree \
                    or tag_part == second_level_tree + 1 and mode == 2\
                    or tag_part == third_level_tree \
                    or tag_part == third_level_tree + 1 and mode == 2 \
                    or tag_part == fourth_level_tree \
                    or tag_part == fourth_level_tree + 1 and mode == 2 \
                    or not g_tag[tag_part].isalpha() \
                    or tag_part >= last_digit:
                tag += g_tag[tag_part]

        if tag not in list_matrix:
            list_matrix.append(tag)  # create first dictionary entry at tag
            is_item_digits_found = 1  # signal continue searching
        else:
            # duplicate found aborting this search
            print('duplicate tag found {} g_tag {} last_digit {}'.format(tag, g_tag, last_digit))

    return is_item_digits_found


def send_tree_part(g_tag, data_base, mode, schema):
    # search_digit == 0
    matrix0 = data_base[0]
    matrix = data_base[1]
    equip_level_tree = matrix0[0]
    first_level_tree = matrix0[1]
    second_level_tree = matrix0[2]
    third_level_tree = matrix0[3]
    fourth_level_tree = matrix0[4]

    equip_type_count_matrix = data_base[2]
    equip_matrix = data_base[3]

    eq_part = g_tag[equip_level_tree]
    if eq_part not in equip_matrix:
        equip_matrix.append(eq_part)
        equip_type_count_matrix.append(0)

    index = equip_matrix.index(eq_part)
    equip_type_count_matrix[index] += 1

    for tag_part in range(0, len(schema)):
        if not fourth_level_tree == tag_part \
                and not third_level_tree == tag_part \
                and not second_level_tree == tag_part \
                and not first_level_tree == tag_part \
                and not equip_level_tree == tag_part:
            if index not in matrix:
                matrix[index] = dict()  # append an empty dict for equip index position

            if mode < 1:
                mode = 1  # set to 1 chr read in mode

            if tag_part + mode > len(schema):
                return

            if mode == 2 and not schema[tag_part: tag_part + 2] == 'NN':
                return
            elif not schema[tag_part: tag_part + 1].isalpha():
                return

            dict_matrix = matrix[index]  # get list containing branches for this equipment

            area = g_tag[tag_part]
            if mode == 2:
                area = area + g_tag[tag_part + 1]

            if tag_part not in dict_matrix:
                dict_matrix[tag_part] = {area: 0}  # create first dictionary entry at tag_part

            if area not in dict_matrix[tag_part]:
                dict_matrix[tag_part][area] = 0

            dict_matrix[tag_part][area] += 1


def send_tag_to_matrix(search_digit, g_tag, schema, data_base, mode, cluster):
    is_item_digits_found = 1

    if search_digit == 0:
        send_tree_part(g_tag, data_base, mode, schema)

    if search_digit == 1:
        is_item_digits_found = send_item_parts(g_tag, data_base, mode, schema, cluster)

    if search_digit == 2:
        send_equipment(g_tag, data_base, mode, cluster)

    return is_item_digits_found


def move_scenario_data_to_array(search_digit, file_name, loc_tagname, loc_cluster, max_count, schema,
                                data_base, mode):
    matrix0 = data_base[0]  # preserve matrix0 ie tree position
    matrix = dict()  # wipe matrix

    if search_digit == 0:
        equip_matrix = []
        equip_type_count_matrix = []
    else:
        equip_type_count_matrix = data_base[2]
        equip_matrix = data_base[3]

    data_base = [matrix0, matrix, equip_type_count_matrix, equip_matrix]

    is_item_digits_found = 0
    read_in_record_count = -1
    count = 0
    with open(file_name, mode='rt', encoding='utf-8') as f:
        for read_line in f:
            read_in_record_count += 1
            if read_in_record_count > 0:
                tag = tag_utils.read_in_data(loc_tagname, read_line.strip()).strip('"')
                cluster = tag_utils.read_in_data(loc_cluster, read_line.strip()).strip('"')
                current_schema, g_tag = tag_utils.get_schema(tag)

                generalised_schema = encode_decode_map_schema.generalise_schema(matrix0, mode, schema)
                generalised_current_schema = encode_decode_map_schema.generalise_schema(matrix0, mode, current_schema)
                if generalised_current_schema.find(generalised_schema) == 0:
                    is_item_digits_found = send_tag_to_matrix(search_digit, g_tag, current_schema,
                                                              data_base, mode, cluster)
                    if not is_item_digits_found:
                        break

                    count += 1
                    if count == max_count:
                        break

    if search_digit == 2:
        print('For schema {} tags read in {} out of {}. ie {} % coverage'
              .format(schema, count, read_in_record_count, 100 * count / read_in_record_count))

    return data_base, is_item_digits_found
