import encode_decode_map_schema
import tag_utils


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

    tree = cluster + ":"
    tree += tag_utils.add_equip_part(g_tag, first_level_tree, mode)
    if tree not in matrix_list:
        matrix_list.append(tree)

    if second_level_tree >= 0:
        tree += '.' + tag_utils.add_equip_part(g_tag, second_level_tree, mode)
        if tree not in matrix_list:
            matrix_list.append(tree)

    if third_level_tree >= 0:
        tree += '.' + tag_utils.add_equip_part(g_tag, third_level_tree, mode)
        if tree not in matrix_list:
            matrix_list.append(tree)

    if fourth_level_tree >= 0:
        tree += '.' + tag_utils.add_equip_part(g_tag, fourth_level_tree, mode)
        if tree not in matrix_list:
            matrix_list.append(tree)


def send_item_parts(g_tag, data_base, mode, schema, cluster):
    # search_digit == 1
    matrix0 = data_base[0]
    equip_level_tree = matrix0[0]
    last_digit = matrix0[5]

    matrix = data_base[1]

    equip_matrix = data_base[3]

    eq_part = g_tag[equip_level_tree]

    if eq_part not in equip_matrix:
        equip_matrix.append(eq_part)

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
        if tag_utils.is_tag_part_used(tag_part, schema, matrix0, mode) or tag_part >= last_digit:
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

    equip_type_count_matrix = data_base[2]
    equip_matrix = data_base[3]

    eq_part = g_tag[equip_level_tree]
    if first_level_tree == -1:
        if eq_part not in equip_matrix:
            equip_matrix.append(eq_part)
            equip_type_count_matrix.append(0)

        index = equip_matrix.index(eq_part)
        equip_type_count_matrix[index] += 1
    else:
        eq_part += '.' + tag_utils.add_equip_part(g_tag, first_level_tree, mode)

        if second_level_tree >= 0:
            eq_part += '.' + tag_utils.add_equip_part(g_tag, second_level_tree, mode)

        if third_level_tree >= 0:
            eq_part += '.' + tag_utils.add_equip_part(g_tag, third_level_tree, mode)

    if eq_part in equip_matrix:
        index = equip_matrix.index(eq_part)
        for tag_part in range(0, len(schema)):
            if not tag_utils.is_tag_part_used(tag_part, schema, matrix0, mode):
                if mode < 1:
                    mode = 1  # set to 1 chr read in mode

                if tag_part + mode > len(schema):
                    continue

                if mode == 2 and not schema[tag_part: tag_part + 2] == 'NN':
                    continue
                elif not schema[tag_part: tag_part + 1].isalpha():
                    continue

                area = tag_utils.add_equip_part(g_tag, tag_part, mode)

                if index not in matrix:
                    matrix[index] = dict()  # append an empty dict for equip index position

                dict_matrix = matrix[index]  # get list containing branches for this equipment

                if tag_part not in dict_matrix:
                    dict_matrix[tag_part] = {area: 0}  # create first dictionary entry at tag_part

                if area not in dict_matrix[tag_part]:
                    dict_matrix[tag_part][area] = 0

                dict_matrix[tag_part][area] += 1


def send_tag_to_matrix(search_digit, g_tag, schema, data_base, mode, cluster):
    is_item_digits_found = 1

    if search_digit == 0:
        # find the area part of tree
        send_tree_part(g_tag, data_base, mode, schema)

    if search_digit == 1:
        # find the item part of tree
        is_item_digits_found = send_item_parts(g_tag, data_base, mode, schema, cluster)

    if search_digit == 2:
        # make a flat list of all equipment
        send_equipment(g_tag, data_base, mode, cluster)

    return is_item_digits_found


def move_scenario_data_to_array(search_digit, file_name, loc_tagname, loc_cluster, max_count, schema,
                                data_base, mode):
    matrix0 = data_base[0]  # preserve matrix0 ie tree position
    first_level_tree = matrix0[1]
    matrix = dict()  # wipe matrix

    if not search_digit == 0 or first_level_tree == - 1:
        equip_matrix = []
        equip_type_count_matrix = []
    else:  # maintain old equipment only when building tree structure but wipe if no tree structure yet
        equip_type_count_matrix = data_base[2]
        equip_matrix = data_base[3]

    data_base = [matrix0, matrix, equip_type_count_matrix, equip_matrix]

    if search_digit == 2:
        _, _, generalised_schema = encode_decode_map_schema.decode_mapping_schema(schema)
    else:
        generalised_schema = encode_decode_map_schema.generalise_schema(matrix0, mode, schema)

    is_item_digits_found = 0
    read_in_record_count = -1
    count = 0
    with open(file_name, mode='rt', encoding='utf-8') as f:
        for read_line in f:
            read_in_record_count += 1
            if read_in_record_count > 0:
                tag = tag_utils.read_in_data(loc_tagname, read_line.strip())
                cluster = tag_utils.read_in_data(loc_cluster, read_line.strip())

                current_schema, g_tag = tag_utils.get_schema(tag)

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


def test_compare_file_headers(file_path, file1, file2):
    with open(file_path + '\\' + file1, mode='rt', encoding='utf-8') as f:
        for read_line_file1 in f:
            break

    with open(file_path + '\\' + file2, mode='rt', encoding='utf-8') as f:
        for read_line_file2 in f:
            break

    line_file1 = read_line_file1.rsplit(',')
    line_file2 = read_line_file2.rsplit(',')
    is_valid = 1
    for index in range(len(line_file1)):
        if line_file1[index] not in line_file2:
            is_valid = 0
            print('file {} field {} not found in file {} header'.
                  format(file1, line_file1[index].strip('\n'), file2))

    for index in range(len(line_file1)):
        if not line_file1[index] == line_file2[index]:
            is_valid = 0
            print('file {} field {} not found in same position in file {}'.
                  format(file1, line_file1[index].strip('\n'), file2))

    return is_valid
