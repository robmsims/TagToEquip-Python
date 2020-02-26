def store_equip(matrix_list, tree):
    if tree not in matrix_list:
        matrix_list.append(tree)


def send_equipment(g_tag, data_base, mode):
    first_level_tree = data_base[0][1]
    second_level_tree = data_base[0][2]
    third_level_tree = data_base[0][3]
    fourth_level_tree = data_base[0][4]

    matrix_list = data_base[1][0]

    tree = g_tag[first_level_tree]
    if mode == 2:
        tree = tree + g_tag[first_level_tree + 1]
    store_equip(matrix_list, tree)

    if second_level_tree >= 0:
        tree = tree + '.' + g_tag[second_level_tree]
        if mode == 2:
            tree = tree + g_tag[second_level_tree + 1]
        store_equip(matrix_list, tree)

    if third_level_tree >= 0:
        tree = tree + '.' + g_tag[third_level_tree]
        if mode == 2:
            tree = tree + g_tag[third_level_tree + 1]
        store_equip(matrix_list, tree)

    if fourth_level_tree >= 0:
        tree = tree + '.' + g_tag[fourth_level_tree]
        if mode == 2:
            tree = tree + g_tag[fourth_level_tree + 1]
        store_equip(matrix_list, tree)


def send_item_parts(index, g_tag, data_base, mode, schema, cluster):
    equip_level_tree = data_base[0][0]
    first_level_tree = data_base[0][1]
    second_level_tree = data_base[0][2]
    third_level_tree = data_base[0][3]
    fourth_level_tree = data_base[0][4]
    last_digit = data_base[0][5]

    char = schema[last_digit:last_digit + 1]
    if not char.isalpha():
        is_item_digits_found = 0  # abort search for duplicates as we have a delineator
        #print('abort delineator found {} {}'.format(char,g_tag))
        return is_item_digits_found

    matrix = data_base[1]  # get list of dictionary elements list
    list_matrix = matrix[index]  # get list containing tags for this equipment

    is_item_digits_found = 1
    tag = cluster+"."
    for tag_part in range(0, len(schema)):  # only record on first part of item
        add_digit = 0
        if tag_part == equip_level_tree:
            add_digit = 1
        elif tag_part == first_level_tree:
            add_digit = 1
        elif tag_part == first_level_tree+1 and mode == 2:
            add_digit = 1
        elif tag_part == second_level_tree:
            add_digit = 1
        elif tag_part == second_level_tree+1 and mode == 2:
            add_digit = 1
        elif tag_part == third_level_tree:
            add_digit = 1
        elif tag_part == third_level_tree+1 and mode == 2:
            add_digit = 1
        elif tag_part == fourth_level_tree:
            add_digit = 1
        elif tag_part == fourth_level_tree+1 and mode == 2:
            add_digit = 1
        elif tag_part >= last_digit:
            add_digit = 1

        if add_digit == 1:
            tag = tag + g_tag[tag_part]

    if tag not in list_matrix:
        list_matrix.append(tag)  # create first dictionary entry at tag
        #print('stroring tag {}'.format(tag))
    else:
        is_item_digits_found = 0  # duplicate found aborting this search
        #print('duplicate tag found {} g_tag {} last_digit {}'.format(tag, g_tag, last_digit))

    return is_item_digits_found

def send_tree_part(tag_part, index, g_tag, data_base, mode, schema):
    if mode < 1:
        mode = 1  # set to 1 chr read in mode

    if tag_part + mode > len(schema):
        return
    elif not schema[tag_part+1: tag_part + 2]=='N' and mode == 2:
        return

    if not schema[tag_part: tag_part + 1]=='N':
        return

    matrix = data_base[1]  # get list of dictionary elements list
    dict_matrix = matrix[index]  # get list containing branches for this equipment

    area = g_tag[tag_part]
    if mode == 2:
        area = area + g_tag[tag_part+1]

    if tag_part not in dict_matrix:
        dict_matrix[tag_part] = {area: 0}  # create first dictionary entry at tag_part

    if area not in dict_matrix[tag_part]:
        dict_matrix[tag_part][area] = 0

    dict_matrix[tag_part][area] += 1


def send_tag_to_matrix(search_digit, g_tag, schema, data_base, mode, cluster):
    matrix0 = data_base[0]
    equip_level_tree = matrix0[0]
    first_level_tree = matrix0[1]
    second_level_tree = matrix0[2]
    third_level_tree = matrix0[3]
    fourth_level_tree = matrix0[4]

    matrix = data_base[1]
    is_item_digits_found = 1

    equip_type_count_matrix = data_base[2]
    equip_matrix = data_base[3]

    eq_part = g_tag[equip_level_tree]

    if first_level_tree == -1 or not search_digit == 0:
        if eq_part not in equip_matrix:
            equip_matrix.append(eq_part)
            equip_type_count_matrix.append(0)

        index = equip_matrix.index(eq_part)
        equip_type_count_matrix[index] += 1
    else:
        if first_level_tree >= 0:
            eq_part = eq_part + '.' + g_tag[first_level_tree]
            if mode == 2:
                eq_part = eq_part + g_tag[first_level_tree + 1]

        if second_level_tree >= 0:
            eq_part = eq_part + '.' + g_tag[second_level_tree]
            if mode == 2:
                eq_part = eq_part + g_tag[second_level_tree + 1]

        if third_level_tree >= 0:
            eq_part = eq_part + '.' + g_tag[third_level_tree]
            if mode == 2:
                eq_part = eq_part + g_tag[third_level_tree + 1]

    if eq_part not in equip_matrix:
        return is_item_digits_found

    index = equip_matrix.index(eq_part)


    if index not in matrix:
        if search_digit == 0:
            matrix[index] = dict()  # append an empty dict for equip index position
        else:
            matrix[index] = list()  # append an empty list for equip index position

    if search_digit == 0:  # tree search mode
        for tag_part in range(0, len(schema)):
            if not fourth_level_tree == tag_part:
                if not third_level_tree == tag_part:
                    if not second_level_tree == tag_part:
                        if not first_level_tree == tag_part:
                            if not equip_level_tree == tag_part:
                                send_tree_part(tag_part, index, g_tag, data_base, mode, schema)
    elif search_digit == 1:
        is_item_digits_found = send_item_parts(index, g_tag, data_base, mode, schema, cluster)
    elif search_digit == 2:
        send_equipment(g_tag, data_base, mode)
        is_item_digits_found = 1  # force continue

    return is_item_digits_found


def read_in_data(data_loc, line_str):
    record_list = line_str.rsplit(',')
    return record_list[data_loc]


def get_schema(tag):
    schema = ''
    type = ''
    g_tag = []

    for char in tag:
        if char.isalpha():
            if not type == "W":
                type = "W"
                schema = schema + type
                g_tag.append(char)
            else:
                g_tag[len(g_tag ) - 1] = g_tag[len(g_tag ) - 1] + char

        if char.isnumeric():
            type = "N"
            schema = schema + type
            g_tag.append(char)

        if not char.isalnum():
            type = char  # record delineator type
            schema = schema + type
            g_tag.append(char)

    return schema, g_tag


def move_scenario_data_to_array(search_digit, file_name, loc_tagname, loc_cluster, max_count, schema,
                                data_base, mode):

    matrix0 = data_base[0]
    equip_level_tree = matrix0[0]
    first_level_tree = matrix0[1]
    second_level_tree = matrix0[2]
    third_level_tree = matrix0[3]
    fourth_level_tree = matrix0[4]

    matrix = dict()

    equip_type_count_matrix = data_base[2]
    equip_matrix = data_base[3]
    if first_level_tree == -1 or not search_digit == 0:
        equip_matrix = []
        equip_type_count_matrix = []

    data_base = [matrix0, matrix, equip_type_count_matrix, equip_matrix]

    is_item_digits_found = 0
    read_in_record_count = 0
    count = 0
    with open(file_name, mode='rt', encoding='utf-8') as f:
        for read_line in f:
            read_in_record_count += 1
            if read_in_record_count > 1:
                tag = read_in_data(loc_tagname, read_line.strip()).strip('"')
                cluster = read_in_data(loc_cluster, read_line.strip()).strip('"')
                current_schema, g_tag = get_schema(tag)

                if search_digit == 1:
                    last_digit = data_base[0][5]
                    schema = schema[0:last_digit]

                if current_schema.find(schema) == 0:
                    is_item_digits_found = send_tag_to_matrix(search_digit, g_tag, current_schema,
                                                              data_base, mode, cluster)
                    if not is_item_digits_found:
                        break

                    count += 1
                    if count == max_count:
                        break

    if search_digit == 2:
        print('For schema {} tags read in {} out of {}. ie {} % coverage'
              .format(schema, count, read_in_record_count, 100*count/read_in_record_count))

    return data_base, is_item_digits_found