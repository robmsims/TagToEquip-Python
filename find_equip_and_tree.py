import count_equip
import tag_utils
import read_csv_file


def find_best_match_for_tree(schema, data_base, dont_use_words, percent_filter, mode):
    filter_min = 92
    if percent_filter < filter_min:
        filter_min = percent_filter

    score_total_max = 0
    tag_part_at_max = -1
    for current_filter in range(percent_filter, filter_min - 1, -1):
        score_total_max = 0
        score_total_prev = 0
        for tag_part in range(0, len(schema)):
            char = schema[tag_part:tag_part + 1]
            if char == "W" and dont_use_words == 1:
                continue

            if not char.isalpha():
                continue

            score_total, score_total_count, score_total_num_stored, score_total_num_of_areas_used = \
                count_equip.add_highest_count_of_stored_tree_parts(
                        tag_part, data_base, score_total_prev, current_filter, schema, mode)

            if score_total_max < score_total:
                score_total_prev = score_total_max  # record previous max
                score_total_max = score_total
                tag_part_at_max = tag_part
            elif score_total_prev < score_total:
                score_total_prev = score_total  # if two scores are the same record second as prev

        if not score_total_max == 0:
            if score_total_prev / score_total_max < percent_filter / 100.0:
                break

    return tag_part_at_max, score_total_max


def read_in_schema(file_name, loc_tagname, max_count):
    data_block = []
    with open(file_name, mode='rt', encoding='utf-8') as f:
        read_count = 0
        for read_line in f:
            if read_count > 0:
                tag = tag_utils.read_in_data(loc_tagname, read_line.strip())
                # g_tag not used here but required by function get_schema
                current_schema, g_tag = tag_utils.get_schema(tag)
                data_block.append(current_schema)

            read_count += 1
            if read_count > max_count:
                break

    last_schema = ''
    schema = ''
    top_count = 0
    count = 0
    data_block.sort()
    for current_schema in data_block:
        if not last_schema == current_schema:
            count = 0  # reset count on change of schema

        last_schema = current_schema
        count += 1
        if count > top_count:
            top_count = count
            schema = current_schema

    return schema


def find_equip_type_position_and_import_data(file_name, loc_tagname, loc_cluster, max_count,
                                             schema, mode, percent_filter):
    word_count = 0
    for char in schema:
        if char == "W":
            word_count += 1

    matrix0 = [-1, -1, -1, -1, -1, -1, -1, -1]  # initialize area hierarchy
    matrix = []
    equip_type_count_matrix = []
    equip_matrix = []
    data_base = [matrix0, matrix, equip_type_count_matrix, equip_matrix]  # initiate a new database

    search_digit = 0

    count_total_max = 0
    count_total_prev = 0

    first_level_tree_max = -1
    equip_postion_max = -1

    equip_level_tree = -1
    for current_equip_postion in range(1, word_count + 1):
        count = 0
        equip_level_tree = 0
        for char in schema:
            equip_level_tree += 1
            if char == "W":
                count += 1
                if count == current_equip_postion:
                    break

        equip_level_tree -= 1
        data_base[0][0] = equip_level_tree
        data_base, _ = read_csv_file.move_scenario_data_to_array(search_digit, file_name, loc_tagname, loc_cluster,
                                                                 max_count, schema, data_base, mode)
        dont_use_words = 0
        first_level_tree, count_total = find_best_match_for_tree(schema, data_base,
                                                                 dont_use_words, percent_filter, mode)
        if count_total > count_total_max:
            count_total_prev = count_total_max
            count_total_max = count_total
            equip_postion_max = equip_level_tree
            first_level_tree_max = first_level_tree
        elif count_total > count_total_prev:
            count_total_prev = count_total

    # compare highest core with next highest score
    if not count_total_max == 0:
        if count_total_prev / count_total_max <= percent_filter / 10.0:  # se to 10 to force schema
            if not equip_postion_max == equip_level_tree:  # reload array if different pos
                data_base[0][0] = equip_postion_max
                data_base, _ = read_csv_file.move_scenario_data_to_array(
                    search_digit, file_name, loc_tagname, loc_cluster, max_count, schema, data_base, mode)

            data_base[0][1] = first_level_tree_max

    if data_base[0][1] == -1:
        data_base[0][0] = -1  # equipment position not found flag
        print('error scoring for different schema positions is too similar. score_total_prev {} score_total_max {}'
              .format(count_total_prev, count_total_max))

    return data_base


def find_tree(file_name, schema, data_base, loc_tagname, loc_cluster, max_count, mode, score_filter, percent_filter):
    search_digit = 0
    dont_use_words = 1
    first_level_tree = data_base[0][1]

    data_base = count_equip.filter_equipment(data_base, first_level_tree, score_filter)
    data_base, _ = read_csv_file.move_scenario_data_to_array(search_digit, file_name, loc_tagname, loc_cluster,
                                                             max_count, schema, data_base, mode)
    second_level_tree, count_total = find_best_match_for_tree(schema, data_base,
                                                              dont_use_words, percent_filter, mode)
    if second_level_tree >= 0:
        data_base[0][2] = second_level_tree

        data_base = count_equip.filter_equipment(data_base, second_level_tree, percent_filter)
        data_base, _ = read_csv_file.move_scenario_data_to_array(search_digit, file_name, loc_tagname, loc_cluster,
                                                                 max_count, schema, data_base, mode)
        third_level_tree, count_total = find_best_match_for_tree(schema, data_base,
                                                                 dont_use_words, percent_filter, mode)
        if third_level_tree >= 0:
            data_base[0][3] = third_level_tree

            data_base = count_equip.filter_equipment(data_base, third_level_tree, percent_filter)
            data_base, _ = read_csv_file.move_scenario_data_to_array(
                search_digit, file_name, loc_tagname, loc_cluster, max_count, schema, data_base, mode)
            fourth_level_tree, count_total = find_best_match_for_tree(schema, data_base,
                                                                      dont_use_words, percent_filter, mode)
            if fourth_level_tree >= 0:
                data_base[0][4] = fourth_level_tree

    return data_base


def find_item(file_name, loc_tagname, loc_cluster, max_count, schema, data_base, mode):
    equip_level_tree = data_base[0][0]
    first_level_tree = data_base[0][1]
    second_level_tree = data_base[0][2]
    third_level_tree = data_base[0][3]
    fourth_level_tree = data_base[0][4]

    is_item_found = 0
    search_digit = 1
    first_digit = len(schema)-1
    for l_digit in range(first_digit, - 1, -1):
        extra_char = 0
        if mode == 2:
            extra_char = 1

        if l_digit == fourth_level_tree + extra_char:
            data_base[0][4] = -1

        if l_digit == third_level_tree + extra_char:
            data_base[0][4] = -1
            data_base[0][3] = -1

        if l_digit == second_level_tree + extra_char:
            data_base[0][4] = -1
            data_base[0][3] = -1
            data_base[0][2] = -1

        if l_digit == first_level_tree + extra_char:
            data_base[0][4] = -1
            data_base[0][3] = -1
            data_base[0][2] = -1
            data_base[0][1] = -1

        if l_digit == equip_level_tree:
            data_base[0][0] = - 1

        data_base[0][5] = l_digit
        # schema = schema[0:l_digit + 1]
        data_base, is_item_digits_found = read_csv_file.move_scenario_data_to_array(
                            search_digit, file_name, loc_tagname, loc_cluster, max_count, schema, data_base, mode)
        if is_item_digits_found:
            break

    if not data_base[0][1] == - 1:
        data_base[0][2] = second_level_tree
        data_base[0][3] = third_level_tree
        data_base[0][4] = fourth_level_tree
        is_item_found = 1

    return data_base, is_item_found


def find_equipment(schema, data_base):
    equip_num_start = data_base[0][5]
    search_end = len(schema) - 1

    is_equip_num_found = 0
    if equip_num_start < search_end:
        next_char = ''
        index = len(schema) - 1
        for index in range(equip_num_start, search_end - 1):
            current_char = schema[index:index + 1]
            next_char = schema[index + 1:index + 2]
            if not current_char == next_char:
                is_equip_num_found = 1
                break

        if is_equip_num_found:
            if not next_char.isalnum():  # not alphanumeric
                if index + 2 <= search_end:
                    data_base[0][5] = index + 2  # index
                    data_base[0][6] = equip_num_start
                    data_base[0][7] = index   # end of number part

            else:
                data_base[0][5] = index + 1  # index
                data_base[0][6] = equip_num_start
                data_base[0][7] = index  # end of number part

    return data_base
