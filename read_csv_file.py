def send_tree_part(tag_part, eq_part, index, g_tag, data_base, mode, schema, first_level_tree):
    #print('position {}  {}'.format(tag_part, g_tag[tag_part]))

    if mode < 1:
        mode = 1 # set to 1 chr read in mode

    if tag_part + mode > len(schema):
        return
    elif not schema[tag_part+1: tag_part + 2]=='N' and mode == 2:
        return

    if not schema[tag_part: tag_part + 1]=='N':
        return

    #print(schema[tag_part: tag_part + 1])

    matrix0 = data_base[0] # get count of element types list
    matrix = data_base[1] # get list of dictionary elements list

    dict_matrix0 = matrix0[index] # get list containing branches for this equipment
    dict_matrix = matrix[index] # get list containing branches for this equipment

    area = g_tag[tag_part]
    if mode == 2:
        area = area + g_tag[tag_part+1]

    if not tag_part in dict_matrix0:
        dict_matrix0[tag_part] = 1
        dict_matrix[tag_part] = {area:0}

    if not area in dict_matrix[tag_part]:
        dict_matrix[tag_part][area] = 0
        dict_matrix0[tag_part] += 1

    dict_matrix[tag_part][area] += 1

    #print('tag_part {} area {} len {} count {}'
    #      .format(tag_part, area, dict_matrix0[tag_part], area_dict_matrix))
    #print('eqpipment {}, count {}'.format(data_base[1][0], data_base[0][0]))

    return

def send_tag_to_matrix(search_digit, g_tag, schema,
                    equip_postion, data_base, mode,
                    first_level_tree, second_level_tree,
                    third_level_tree, fourth_level_tree):

    matrix0 = data_base[0]
    matrix = data_base[1]
    equip_type_count_matrix = data_base[2]
    equip_matrix = data_base[3]

    count = 0
    equip_level_tree = 0
    for char in schema:
        equip_level_tree += 1
        if char == "W":
            count += 1
            if count == equip_postion:
                break

    equip_level_tree -= 1
    tag_equip_part = equip_level_tree
    eq_part = g_tag[equip_level_tree]
    #print('eqpipment {}, pos {}'.format(eq_part, equip_postion))

    if first_level_tree == -1:
        if not eq_part in equip_matrix:
            equip_matrix.append(eq_part)
            equip_type_count_matrix.append(0)
            matrix0.append(dict())
            matrix.append(dict())

        index = equip_matrix.index(eq_part)
        equip_type_count_matrix[index] += 1
        #print('eqpipment {}, pos {}'.format(equip_matrix, equip_postion))
        #print('eqpipment {}, count {}'.format(equip_matrix, equip_type_count_matrix[index]))
        #print(equip_type_count_matrix)

    index = equip_matrix.index(eq_part)
    for tag_part in range(0, len(schema)):
        if not fourth_level_tree == tag_part:
            if not third_level_tree == tag_part:
                if not second_level_tree == tag_part:
                    if not first_level_tree == tag_part:
                        if not equip_level_tree == tag_part:
                            if search_digit == 0:
                                send_tree_part(tag_part, eq_part, index, g_tag,
                                                            data_base, mode,
                                                            schema, first_level_tree)

    return


def read_in_data(data_loc, line_str):
    record_list = line_str.rsplit(',')
    return record_list[data_loc]


def get_schema(tag):
    schema = ''
    type = ''
    g_tag = []

    for char in tag:
        if char == "\"":
            continue

        # print('character {}'.format(chr)) - for debugging
        if char.isalpha():
            if not type == "W":
                type = "W"
                schema = schema + type
                g_tag.append(char)
            else:
                g_tag[len(g_tag ) -1] = g_tag[len(g_tag ) -1] + char

        if char.isnumeric():
            type = "N"
            schema = schema + type
            g_tag.append(char)

        if not char.isalnum():
            type = char # record delineator type
            schema = schema + type
            g_tag.append(char)

    # print('g_tag = {}'.format(g_tag)) # for debuging
    return schema, g_tag


def move_scenario_data_to_array(search_digit, file_name, loc_tagname, max_count, schema,
                                equip_postion, data_base, mode,
                                first_level_tree=-1, second_level_tree=-1,
                                third_level_tree=-1, fourth_level_tree=-1):

    matrix0 = []
    matrix = []

    equip_type_count_matrix = data_base[2]
    equip_matrix = data_base[3]
    if first_level_tree == -1:
        equip_matrix = []
        equip_type_count_matrix = []

    data_base = [matrix0, matrix, equip_type_count_matrix, equip_matrix]

    for index in range(2):
        read_in_record_count = 0
        count = 0
        with open(file_name, mode='rt', encoding='utf-8') as f:
            for read_line in f:
                if read_in_record_count > 0:
                    tag = read_in_data(loc_tagname, read_line.strip())
                    current_schema, g_tag = get_schema(tag)
                    if current_schema == schema:
                        # print('tag = {}'.format(tag))
                        send_tag_to_matrix(search_digit, g_tag, schema,
                                            equip_postion, data_base, mode,
                                            first_level_tree, second_level_tree,
                                            third_level_tree, fourth_level_tree)

                        count += 1
                        if count == max_count:
                            break
                read_in_record_count += 1

        if search_digit == 0:
            break

    #print('eqpipment {}, pos {}'.format(data_base[3], equip_postion))
    #print('eqpipment {}, count {}'.format(data_base[1][0], data_base[0][0]))

    return data_base