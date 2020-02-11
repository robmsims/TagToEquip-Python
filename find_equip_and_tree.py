import read_csv_file
import count_equip

def find_best_match_for_tree(schema, data_base, dont_use_words, percent_filter):
    filter_min = 92
    if percent_filter < filter_min:
        filter_min = percent_filter

    score_total_max = 0
    tag_part_at_max = -1
    for current_filter in range(percent_filter, filter_min-1, -1):
        score_total_max = 0
        score_total_prev = 0
        for tag_part in range(0,len(schema)):
            char = schema[tag_part:tag_part+1]
            if char == "W" and dont_use_words == 1:
                continue

            if not char.isalpha():
                continue

            score_total = count_equip.add_highest_count_of_stored_tree_parts(tag_part,
                                            data_base, score_total_max, current_filter)

            if score_total_max < score_total:
                if score_total_prev < score_total_max:
                    score_total_prev = score_total_max  # record previous max
                    
                score_total_max = score_total
                tag_part_at_max = tag_part

            elif score_total_prev < score_total:
                score_total_prev = score_total  # if two scores are the same record second as prev

        if not score_total_max == 0:
            if score_total_prev/score_total_max < percent_filter/100.0:
                break

    return tag_part_at_max, score_total_max


def read_first_line(file_name):
    with open(file_name, mode='rt', encoding='utf-8') as f:
        return f.readline().strip().lower().rsplit(',')


def read_in_schema(file_name, loc_tagname, max_count):
    data_block = []
    with open(file_name, mode='rt', encoding='utf-8') as f:
        read_count = 0
        for read_line in f:
            if read_count > 0:
                tag = read_csv_file.read_in_data(loc_tagname, read_line.strip())
                # g_tag not used here but required by function get_schema
                current_schema, g_tag = read_csv_file.get_schema(tag)
                data_block.append(current_schema)

            read_count += 1
            if read_count > max_count:
                break

    last_schema = ''
    top_count = 0
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


def find_equip_type_position_and_import_data(file_name, loc_tagname, max_count, schema, mode, percent_filter):
    count = 0
    for chr in schema:
        if chr == "W":
            count += 1

    matrix0 = [-1,-1,-1,-1,-1]  # initalise area hirearchey
    matrix = []
    equip_type_count_matrix = []
    equip_matrix = []
    data_base = [matrix0, matrix, equip_type_count_matrix, equip_matrix]  # initiate a new database

    search_digit = 0

    count_total_max = -1
    first_level_tree_max = -1
    equip_postion_max = -1

    current_equip_postion = -1
    for current_equip_postion in range(1,count+1):
        data_base[0][0] = current_equip_postion
        data_base = read_csv_file.move_scenario_data_to_array(search_digit, file_name, loc_tagname,
                                                    max_count, schema, data_base, mode)

        dont_use_words = 1
        first_level_tree, count_total = find_best_match_for_tree(schema, data_base,
                                                            dont_use_words, percent_filter)
        print('word {}, score_total_max {}'.format(current_equip_postion, count_total))
        if count_total > count_total_max:
            count_total_max = count_total
            equip_postion_max = current_equip_postion
            first_level_tree_max = first_level_tree

    if not equip_postion_max == current_equip_postion:  # reload array if different pos
        data_base[0][0] = equip_postion_max
        data_base = read_csv_file.move_scenario_data_to_array(search_digit, file_name, loc_tagname,
                                                  max_count, schema, data_base, mode)

    data_base[0][1] = first_level_tree_max
    return data_base

def find_tree(file_name, schema, data_base, loc_tagname, max_count, mode, filter, percent_filter):
    search_digit = 0
    dont_use_words = 1
    equip_postion = data_base[0][0]
    first_level_tree = data_base[0][1]

    print('first level is at schema position {}'.format(first_level_tree+1))  # convert to 1 base

    data_base = count_equip.filter_equipment(data_base, first_level_tree, filter)
    data_base = read_csv_file.move_scenario_data_to_array(search_digit, file_name, loc_tagname,
                                                          max_count, schema, data_base, mode)
    second_level_tree, count_total = find_best_match_for_tree(schema, data_base,
                                                             dont_use_words, percent_filter)
    if second_level_tree >= 0:
        data_base[0][2] = second_level_tree
        print('second level is at schema position {}'.format(second_level_tree+1))  # convert to 1 base

        data_base = count_equip.filter_equipment(data_base, second_level_tree, percent_filter)
        data_base = read_csv_file.move_scenario_data_to_array(search_digit, file_name, loc_tagname,
                                                              max_count, schema, data_base, mode)
        third_level_tree, count_total = find_best_match_for_tree(schema, data_base,
                                                                 dont_use_words, percent_filter)

    if third_level_tree >= 0:
        data_base[0][3] = third_level_tree
        print('third level is at schema position {}'.format(third_level_tree + 1))  # convert to 1 base

        data_base = count_equip.filter_equipment(data_base, third_level_tree, percent_filter)
        data_base = read_csv_file.move_scenario_data_to_array(search_digit, file_name, loc_tagname,
                                                              max_count, schema, data_base, mode)
        fourth_level_tree, count_total = find_best_match_for_tree(schema, data_base,
                                                                 dont_use_words, percent_filter)

    if fourth_level_tree >= 0:
        data_base[0][4] = fourth_level_tree
        print('fourth level is at schema position {}'.format(fourth_level_tree + 1))  # convert to 1 base

    return data_base